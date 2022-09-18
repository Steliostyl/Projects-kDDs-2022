import node as node
import random
from node import nodes
from node import KS

# Node count
NC = 5

def printNodes():
    for item in nodes.items():
        print(item[1].id)
        for entry in item[1].f_table:
            print(entry[0], "->", entry[1].id)
        print()

def main():
    # Create an array of randomly generated 
    # numbers within the hash space
    random_n = random.sample(range(2**KS), NC)
    print(random_n)

    # Create nodes from randomly generated 
    # numbers and add them to the network
    for a in random_n:
        nodes[a] = node.Node(a)
        node.node_join(nodes[a])
    
    printNodes()

if __name__ == "__main__":
    main()