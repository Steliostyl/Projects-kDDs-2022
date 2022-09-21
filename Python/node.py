import hashlib
import random
import pandas as pd

# Key size (bits)
KS = 4
# Hashing space
HS = 2**KS

def parse_csv(filename: str) -> dict:
    """Parses csv and returns a list of items."""
    items = {}
    df = pd.read_csv(filename)

    for i in range(len(df)):
        key = '_'.join([df.values[i][0], str(df.values[i][2])])
        
        data = {key : {
            'Date': df.values[i][0],
            'Block': df.values[i][1],
            'Plot': df.values[i][2],
            'Experimental_treatment': df.values[i][3],
            'Soil_NH4': df.values[i][4],
            'Soil_NO3': df.values[i][5],
        }}
        items[key] = data
    
    return items

def hash_func(key: str) -> int:
    hash_out = hashlib.sha1()
    hash_out.update(bytes(key.encode("utf-8")))
    return int(hash_out.hexdigest(), 16) % HS

def cw_dist(k1: int, k2: int) -> int:
    """Clockwise distance of 2 keys"""
    
    if k1 <= k2:
        return k2 - k1
    else:
        return (HS) + (k2 - k1)

def comp_cw_dist(k1: int, k2: int, dest: int) -> bool:
    """Returns true if clockwise distance of k1 from dest
    is bigger than clockwise distance of k2 from dest.
    In other words, k2 ∈ (k1, dest]"""

    if cw_dist(k1, dest) > cw_dist(k2, dest):
        return True
    return False

class Node:
    def __init__(self, id: int, pred=None) -> None:
        self.id = id
        # List of dictionaries
        self.items = {}
        # list(table) of lists of the form: [position, node]
        self.f_table = []
        self.pred = pred

    def closest_pre_node(self, key: int) -> 'Node':
        """Returns the last predecessor from THIS node's finger table"""

        current = self
        for i in range(KS):
            # current.successor ∈ (current, key]
            if comp_cw_dist(current.id, current.f_table[i][1].id, key):
                current = current.f_table[i][1]
        return current

    def find_successor(self, key: int) -> 'Node':
        """Returns the node with the shortest
        clockwise distance from the given key"""

        current = self.closest_pre_node(key)
        next = current.closest_pre_node(key)

        while comp_cw_dist(current.id, next.id, key):
            current = next
            next = current.closest_pre_node(key)

        if current.id == key:
            return current

        return current.f_table[0][1]

    def circular_node_search(self, key: int) -> 'Node':
        """Returns the node with the shortest
        clockwise distance from the given key.
        Linear search, used to update f_tables."""

        current = self
        while comp_cw_dist(current.id, current.f_table[0][1].id, key):
            current = current.f_table[0][1]

        if current.id == key:
            return current

        return current.f_table[0][1]

            
    def fix_fingers(self) -> None:
        """Called periodically.
        Refreshes finger table entries."""

        for i in range(KS - 1):
            next_in_finger = self.f_table[i + 1]
            next_in_finger[1] = self.circular_node_search(next_in_finger[0])
        #self.print_node()

    def insert_new_pred(self, new_n: 'Node') -> None:
        """Inserts new node to the network as this node's predecessor.
        Also updates neighboring nodes and necessary finger tables."""
        
        # New node's successor is this node
        new_n.f_table.append([(new_n.id + 1) % (HS), self])
        # Predecessor's new successor is the new node
        self.pred.f_table[0][1] = new_n
        # New node's predecessor is this node's predecessor
        new_n.pred = self.pred
        # This node's predecessor is the new node
        self.pred = new_n

        self.move_items_to_pred()
        new_n.initialize_finger_table()
        new_n.update_necessary_fingers(joinning=True)

    def insert_item(self, new_item: tuple) -> None:
        """Insert data in the node."""
        
        self.items[new_item[0]] = new_item[1]

    def move_items_to_pred(self) -> None:    
        """Moves node's items to predecessor.
        Used after a new node joins the network.
        Assumes all predecessors are up to date."""

        for key in sorted(self.items):
            # key ∉ (previous predecessor, new node (current predecessor)]
            if not comp_cw_dist(self.pred.pred.id, hash_func(key), self.pred.id):
                break
            self.pred.items[key] = self.items[key]
            del self.items[key]

    def initialize_finger_table(self) -> None:
        """Initialize node's finger table.
        Assumes node's successor is up to date."""

        i = 1
        while i < KS:
            pos = (self.id + (2**i)) % (HS)

            # While pos ∈ (new_n.id, new_n.successor]
            while (i < KS) and comp_cw_dist(self.id, pos, self.f_table[0][1].id):
                # new_n [i] = new_n.successor
                self.f_table.append([pos, self.f_table[0][1]])
                i += 1
                pos = (self.id + (2**i)) % (HS)

            if i == KS:
                break

            self.f_table.append([pos, self.f_table[0][1].find_successor(pos)])
            i += 1

    def leave(self) -> None:
        """Removes node from the network."""

        # Move all keys to successor node
        self.f_table[0][1].items = self.f_table[0][1].items | self.items
        # Update successor's predecessor
        self.f_table[0][1].pred = self.pred
        # Update predecessor's successor
        self.pred.f_table[0][1] = self.f_table[0][1]

        self.update_necessary_fingers()
    
    def calc_furth_poss_pred(self) -> int:
        """Calculates the furthest possible predecessor id whose 
        last finger table entry position is equal to or higher
        than the current node's ID."""

        if self.id >= 2**(KS-1):
            return self.id - (2**(KS-1))

        return 2**KS + (self.id-(2**(KS-1)))

    def update_necessary_fingers(self, joinning = False) -> None:
        """Updates necessary finger tables on node join/leave"""

        furthest_possible_pred_id = self.calc_furth_poss_pred()
        next_pred = self.pred
        if next_pred == self or next_pred is None:
            return

        # next_pred.id ∈ (furthest_possible_pred_id, self]
        while comp_cw_dist(furthest_possible_pred_id, next_pred.id, self.id):
            next_pred.fix_fingers()
            next_pred = next_pred.pred
            if next_pred == self or next_pred is None:
                return
            
        if not joinning:
            comp = self
        else:
            comp = self.f_table[0][1]

        # next_pred last = current node
        while next_pred.f_table[KS-1][1] == comp:
            next_pred.fix_fingers()
            next_pred = next_pred.pred
            if next_pred == self or next_pred is None:
                return

    def print_node(self, items_print = False) -> None:
        print(self.id)
        if items_print: 
            print(self.items.keys())
        for entry in self.f_table:
            print(entry[0], "->", entry[1].id)

class Network:
    def __init__(self) -> None:
        self.nodes = []
        
    def build_network(self, node_count: int, node_ids: list = []) -> None:
        if node_ids == []:
            numbers = random.sample(range(HS), node_count)
        else: 
            numbers = node_ids
        for x in numbers:
            new_node = Node(x)
            self.node_join(new_node)
            
    def node_join(self, new_node : Node) -> None:
        # First node.
        if not self.nodes:
            new_node.pred = new_node
            # Initialize finger table.
            new_node.f_table = [ [(new_node.id + 2**i) % HS, new_node] for i in range(KS) ]

        else:
            # Find new node successor and insert the new node before it.
            self.nodes[0].find_successor(new_node.id).insert_new_pred(new_node)

        self.nodes.append(new_node)

    def insert_item(self, new_item: tuple) -> None:
        """Inserts an item (key, value) to the correct node of the network."""

        succ = self.nodes[0].find_successor(hash_func(new_item[0]))
        succ.items[new_item[0]] = new_item[1]
        #print('Inserting item with hashed key:', hash_func(new_item[0]), "to node with ID:", succ.id)
        
    def insert_all_data(self, dict_items) -> None:
        """Inserts all data from parsed csv into the correct nodes."""

        for dict_item in list(dict_items):
            self.insert_item(dict_item)
        
    def update_record(self, new_item : dict) -> None:
        """Updates the record (value) of an item given its key."""

        self.nodes[0].find_successor(hash_func(list(new_item.keys())[0])).insert_item(new_item)
        
    def printNodes(self, items_print = False) -> None:
        """Prints all nodes of the network"""

        print(sorted([nnn.id for nnn in self.nodes]))
        for n in self.nodes:
            n.print_node(items_print=items_print)
            print()

    def update_all_fingers(self):
        """Deprecated. Replaced by update_necessary_fingers in Node class."""

        for node in self.nodes:
            node.fix_fingers()

    def remove_random_node(self) -> str:
        """Removes random node from network and returns its ID"""

        r_i = random.randint(0, len(self.nodes)-1)
        r_id = self.nodes[r_i].id
        self.nodes[r_i].leave()
        del(self.nodes[r_i])
        return r_id