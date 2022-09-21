import node

# Node count
NC = 4

def main():
    # Nodes creation
    interface = node.Interface()
    interface.build_network(NC)
    #nw.build_network(node_count=NC, node_ids=[11, 12, 7, 4])
    
    # Data insertion
    items = node.parse_csv("NH4_NO3.csv")
    interface.insert_all_data(items.items())
    interface.print_all_nodes()

    # Random node removal
    print("Removing node ", interface.remove_random_node())
    interface.print_all_nodes()
    
if __name__ == "__main__":
    main()