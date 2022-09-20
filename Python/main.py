import node

# Node count
NC = 5

def main():
    nw = node.Network()
    nw.build_network(NC)
    
    items = node.parse_csv("../NH4_NO3.csv")
    nw.insert_all_data(items.items())

    nw.printNodes(items_print=True)
    
if __name__ == "__main__":
    main()