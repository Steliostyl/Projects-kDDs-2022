import node

# Node count
NC = 4

def main():
    nw = node.Network()
    nw.build_network(NC)

    test_item = {'test_key' : 'test_value'}
    nw.insert_key(test_item)
    nw.printNodes()
    # print("+++++++++")
    # test_node = Node(6)
    # nw.node_join(test_node)
    # nw.printNodes()
    
if __name__ == "__main__":
    main()