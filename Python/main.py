import node

# Node count
NC = 4

def main():
    # Nodes creation
    nw = node.Network()
    nw.build_network(NC)
    #nw.build_network(node_count=NC, node_ids=[11, 12, 7, 4])
    
    # Data insertion
    items = node.parse_csv("../NH4_NO3.csv")
    nw.insert_all_data(items.items())
    nw.printNodes()

    # Random node removal
    print("Removing node ", nw.remove_random_node())
    nw.printNodes()
    
if __name__ == "__main__":
    main()