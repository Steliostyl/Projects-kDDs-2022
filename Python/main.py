import node

# Node count
NC = 5

def main():
    # Nodes creation
    interface = node.Interface()
    #interface.build_network(NC)
    node_ids=[11, 12, 7, 4]
    interface.build_network(node_count=len(node_ids), node_ids=node_ids)
    
    # Data insertion
    items = node.parse_csv("NH4_NO3.csv")
    interface.insert_all_data(items.items())
    interface.print_all_nodes()

    # Node Join
    interface.node_join(15)

    # Node leave
    interface.remove_node(7)

    interface.print_all_nodes()
    
if __name__ == "__main__":
    main()