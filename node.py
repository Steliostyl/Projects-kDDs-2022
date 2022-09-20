import hashlib
import random
import pandas as pd

def parse_csv(filename):
    """Parses csv and returns a list of items."""
    items = []
    df = pd.read_csv(filename)

    for i in range(len(df)):
        key = '_'.join([df.values[i][0], str(df.values[i][2])])
        
        item = {key : {
            'Date': df.values[i][0],
            'Block': df.values[i][1],
            'Plot': df.values[i][2],
            'Experimental_treatment': df.values[i][3],
            'Soil_NH4': df.values[i][4],
            'Soil_NO3': df.values[i][5],
        }}
        items.append(item)
    
    return items

# Key size (bits)
KS = 4
# Hashing space
HS = 2**KS


def hash_func(key: str):
    hash_out = hashlib.sha1()
    hash_out.update(bytes(key.encode("utf-8")))
    return int(hash_out.hexdigest(), 16) % HS


def cw_dist(k1, k2):
    """Clockwise distance of 2 keys"""
    if k1 <= k2:
        return k2 - k1
    else:
        return (HS) + (k2 - k1)


def comp_cw_dist(k1, k2, dest):
    """Returns true if clockwise distance of k1 from dest
    is bigger than clockwise distance of k2 from dest.
    In other words, k2 ∈ (k1, dest]"""

    if cw_dist(k1, dest) > cw_dist(k2, dest):
        return True
    return False

class Node:
    def __init__(self, id, pred=None):
        self.id = id
        # List of dictionaries
        self.items = {}
        # list(table) of lists of the form: [position, node]
        self.f_table = []
        self.pred = pred
        self.successor = None
        self.network = None

    def closest_pre_node(self, key):
        """Returns the last predecessor from THIS node's finger table"""
        current = self
        for i in range(KS):
            if i >= len(current.f_table):
                print("F_table size", i)
                break
            # current.successor ∈ (current, key]
            if comp_cw_dist(current.id, current.f_table[i][1].id, key):
                current = current.f_table[i][1]
        return current

    def find_successor(self, key):
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

    def circular_node_search(self, key):
        """Returns the node with the shortest
        clockwise distance from the given key.
        Linear search, used to update f_tables."""
        current = self

        while comp_cw_dist(current.id, current.f_table[0][1].id, key):
            current = current.f_table[0][1]

        if current.id == key:
            return current

        return current.f_table[0][1]

            
    def fix_fingers(self):
        """Called periodically.
        Refreshes finger table entries."""
        for i in range(KS - 1):
            next_in_finger = self.f_table[i + 1]
            next_in_finger[1] = self.circular_node_search(next_in_finger[0])

    def insert_new_pred(self, new_n: "Node"):
        """Inserts new predecessor node"""
        # print("Inserting new node", new_n.id, "before node", self.id)
        self.pred.f_table[0][1] = new_n
        new_n.pred = self.pred
        self.pred = new_n

        new_n.f_table.append([(new_n.id + 1) % (HS), self])
        
        # Move successor's items to new node 
        for key in sorted(self.items):
            # Items ∉ (predecessor, new node]
            if not comp_cw_dist(new_n.pred.id, hash_func(key), new_n.id):
                break
            new_n.items[key] = self.items[key]
            del self.items[key]

        # Initialize new node's finger table
        i = 1
        while i < KS:
            pos = (new_n.id + (2**i)) % (HS)

            # While pos ∈ (new_n.id, new_n.successor]
            while (i < KS) and comp_cw_dist(new_n.id, pos, new_n.f_table[0][1].id):
                # new_n [i] = new_n.successor
                new_n.f_table.append([pos, self])
                i += 1
                pos = (new_n.id + (2**i)) % (HS)

            if i == KS:
                break

            new_n.f_table.append([pos, new_n.f_table[0][1].find_successor(pos)])
            i += 1

        for node in self.network.nodes:
            node.fix_fingers()

    def insert_item(self, new_item):
        """Insert data in the node."""
        self.items[list(new_item.keys())[0]] = list(new_item.values())[0]


class Network:
    
    def __init__(self):
        self.nodes = []
        
    def build_network(self, node_count : int):
        
        random_n = random.sample(range(HS), node_count)
        for x in random_n:
            new_node = Node(x)
            self.node_join(new_node)
            
    def node_join(self, new_node : Node):
        
        new_node.network = self
        # First node.
        if not self.nodes:
            new_node.pred = new_node
            new_node.successor = new_node
            # Initialize finger table.
            new_node.f_table = [ [(new_node.id + 2**i) % HS, new_node] for i in range(KS) ]

        else:
            # Find new node successor.
            successor = self.nodes[0].find_successor(new_node.id)
            new_node.successor = successor
            # Recalibrate neighboring nodes and finger tables.
            successor.insert_new_pred(new_node)

        self.nodes.append(new_node)

    def insert_key(self, new_item : dict):
        self.nodes[0].find_successor(hash_func(list(new_item.keys())[0])).insert_item(new_item)
        
    def insert_all_data(self, item_list):
        for item in item_list:
            self.insert_key(item)
        
    def update_record(self, new_item : dict):
        self.nodes[0].find_successor(hash_func(list(new_item.keys())[0])).insert_item(new_item)
        
    def printNodes(self):
        for n in self.nodes:
            print(n.id)
            print(n.items)
            for entry in n.f_table:
                print(entry[0], "->", entry[1].id)
            print()
            