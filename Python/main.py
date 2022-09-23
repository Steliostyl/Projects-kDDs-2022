import node

# Node count
NC = 5

def main():
    # Nodes creation
    interface = node.Interface()
    #interface.build_network(NC)
    node_ids=[1, 3, 5, 8]
    interface.build_network(node_count=len(node_ids), node_ids=node_ids)
    
    # Data insertion
    items = node.parse_csv("NH4_NO3.csv")
    interface.insert_all_data(items.items())
    interface.print_all_nodes()

    # Node Join & Leave
    # interface.node_join(15)
    # interface.remove_node(7)

    interface.print_all_nodes()
    
    # Range & kNN queries
    interface.range_query(3,7)
    interface.knn(3, 5)
    
if __name__ == "__main__":
    main()