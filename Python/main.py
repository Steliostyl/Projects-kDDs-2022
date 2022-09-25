import interface as iff
import random

# Key size (bits)
KS = 20
# Hashing space
HS = 2**KS
# Successor list size
SLS = 3
# Node count
NC = 5

def main():
    # Nodes creation
    interface = iff.Interface()
    #interface.build_network(NC)
    node_ids=[1, 3, 4, 5, 6, 8, 15]
    interface.build_network(node_count=len(node_ids), node_ids=node_ids)

    # Data insertion
    items = iff.parse_csv("NH4_NO3.csv")
    interface.insert_all_data(items.items())
    interface.print_all_nodes(items_print=True)
    input("Press any key to continue...\n")

    # Update record based on key
    random_key = random.sample(sorted(items), 1)[0]
    data = "This is a test string to demonstrate the update record function."
    interface.update_record((random_key, data), start_node_id=4)
    input("Press any key to continue...\n")

    # Delete key
    interface.delete_item(random_key)
    input("Press any key to continue...\n")

    # Key lookup
    lookup = {"key": 6, "start_node_id": 3}
    print(f"Looking up responsible node for key {lookup['key']} starting from node {lookup['start_node_id']}:")
    interface.get_node(lookup["start_node_id"])\
        .find_successor(lookup["key"]).print_node(items_print=True, finger_print=True)
    input("Press any key to continue...\n")

    # Exact match
    exact_match = {"key":6, "start_node_id": 3}
    print(f"Searching node with id {exact_match['key']} starting from node {exact_match['start_node_id']}:")
    interface.exact_match(exact_match["key"], exact_match["start_node_id"]).\
        print_node(items_print=True, finger_print=True)

    # Node Join
    interface.node_join(15)
    interface.print_all_nodes()
    input("Press any key to continue...\n")

    # Node Leave
    interface.node_leave(7)
    interface.print_all_nodes()
    input("Press any key to continue...\n")
    
    # Range query
    rq = {"start": 3, "end": 6}
    print(f"Nodes in range: [{rq['start']}, {rq['end']}]:")
    print([hex(n.id) for n in interface.range_query(rq["start"], rq["end"])])
    input("Press any key to continue...\n")

    # kNN query
    kNN = {"k": 2,"key": 3}
    print(f"{kNN['k']} neighbours of {kNN['key']}:")
    print([hex(n.id) for n in interface.knn(kNN["k"], kNN["key"])])
    input("Press any key to continue...\n")
    
if __name__ == "__main__":
    main()