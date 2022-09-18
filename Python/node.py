import hashlib

# Key size (bits)
KS = 6
# Dictionary of nodes. Structure:
# key: node
nodes = {}


def hash_func(key:str):
    hash_out = hashlib.sha1()
    hash_out.update(bytes(key.encode('utf-8')))
    return int(hash_out.hexdigest(), 16) % KS

def cw_dist(k1, k2):
    """Clockwise distance of 2 keys"""

    if k1 == k2:
        return 0
    elif k1 < k2:
        return k2 - k1
    else:
        return (2**KS) + (k2 - k1)

def comp_cw_dist(k1, k2, dest):
    """Returns true if clockwise distance of k1 from dest
    is bigger than clockwise distance of k2 from dest"""

    if cw_dist(k1, dest) > cw_dist(k2, dest):
        return True
    return False

def node_join(nnode):
    """Adds new node to network"""
    #print("Adding node", nnode.id, "to network.")
    nodes[nnode.id] = nnode

    # Node is alone in the network
    if len(nodes) == 1:
        # Initialize finger table to point at self
        for i in range(KS):
            nnode.f_table.append([(nnode.id+(2**i)) % (2**KS), nnode])
    else:
        # Get root node, find the successor of 
        # new node and then add the new node to it
        list(nodes.items())[0][1].find_successor(nnode.id).insert_new_pred(nnode)

def insert_key(item):
    list(nodes.items())[0][1].find_node(hash_func(item["key"])).insert_item(item)

def update_record(item):
    list(nodes.items())[0][1].find_node(hash_func(item["key"])).update_record(item)

class Node:
    def __init__(self, id):
        self.id = id
        # List of dictionaries 
        self.items = []
        # list(table) of lists of the form: [position, node]
        self.f_table = []
        self.pred = self

    def closest_pre_node(self, key):
        """Returns the last predecessor 
        from THIS node's finger table"""

        current = self
        for i in range(KS):
            #if i >= len(current.f_table):
            #    print("F_table size", i)
            #    break
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
            next = current.closest_pre_node(current, key)
        #print("Find node with key", key, "returned node with id", current.id)
        return current.f_table[0][1]

    def circular_node_search(self, key):
        """Returns the node with the shortest 
        clockwise distance from the given key.
        Linear search, used to update f_tables."""

        current = self
        while comp_cw_dist(current.id, current.f_table[0][1].id, key):
            current = current.f_table[0][1]
        return current
        
    def stabilize(self):
        """Called periodically. Verifies immediate 
        successor and notifies them of self."""

        successor = self.f_table[0][1]
        if comp_cw_dist(self.id, successor.pred.id, successor.id):
            self.f_table[0][1] = successor.pred
        successor.notify(self)

    def notify(self, pred_node):
        """pred_node thinks it might
        be our predecessor."""

        if self.pred is None or comp_cw_dist(self.pred.id, pred_node.id, self.id):
            self.pred = pred_node

    def fix_fingers(self):
        """Called periodically.
        Refreshes finger table entries."""

        for entry in self.f_table: #, entry in enumerate(self.f_table):
            #self.f_table[i][1] = entry[1].circular_node_search(entry[0])
            entry[1] = self.circular_node_search(entry[0])

    def insert_new_pred(self, new_n: "Node"):
        """Inserts new predecessor node"""
        
        self.pred.f_table[0][1] = new_n
        new_n.f_table.append([(new_n.id+1) % (2**KS), self])

        # Move successor's items to new node
        while (self.items != []) and comp_cw_dist(self.id, new_n.id, self.items[0]):
            new_n.insert_item(self.items[0])
            del(self.items[0])

        # Initialize new node's finger table
        for i in range(1, KS):
            pos = (new_n.id+(2**i)) % (2**KS)
            new_n.f_table.append([pos, new_n.f_table[i-1][1].circular_node_search(pos)])
        
        new_n.stabilize()
        for n in list(nodes.items()):
            n[1].fix_fingers()

    def insert_item(self, item):
        """Insert item in the sorted items array."""
        # Can be improved
        i = len(self.items)-1
        tmp_k = self.items[i]
        while tmp_k < item["key"] and i>0:
            i -= 1
        self.items[i-1:i-1] = [item]