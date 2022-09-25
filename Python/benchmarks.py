import interface as iff
from time import perf_counter
import random
from main import KS
from pprint import pprint

HS = 2**KS

def benchmark(NC: int, results: dict) -> dict:
    interface = iff.Interface()

    build_start = perf_counter()
    interface.build_network(NC)
    build_end = perf_counter()

    data_start = perf_counter()
    items = iff.parse_csv("NH4_NO3.csv")
    interface.insert_all_data(items.items())
    data_end = perf_counter()
    #interface.print_all_nodes()

    (leave_n, range_n, kNN_n) = random.sample(sorted(interface.nodes), 3)
    search_key = random.randint(a=0, b=HS-1)
    #print(join_n, leave_n, range_n, kNN_n)
    first_node = interface.get_node()

    # Times for NC Nodes
    # Key lookup 
    query_start = perf_counter()
    lookup = first_node.find_successor(search_key)
    query_end = perf_counter()

    # Node join
    for i in range(HS):
        if i not in interface.nodes:
            join_start = perf_counter()
            interface.node_join(new_node_id=i, start_node_id=first_node.id)
            join_end = perf_counter()
            break

    # Node Leave
    leave_start = perf_counter()
    interface.node_leave(leave_n, first_node.id)
    leave_end = perf_counter()

    # Range query
    range_start = perf_counter()
    rq = interface.range_query(150, 250)
    range_end = perf_counter()

    # kNN query
    knn_start = perf_counter()
    knn = interface.knn(5, kNN_n)
    knn_end = perf_counter()

    results['Build'][NC] = (build_end - build_start)
    results['Data Insertion'][NC] = (data_end - data_start)
    results['Key lookup'][NC] = (query_end - query_start)
    results['Node Join'][NC] = (join_end - join_start)
    results['Node Leave'][NC] = (leave_end - leave_start)
    results['Range Query'][NC] = (range_end - range_start)
    results['kNN Query'][NC] = (knn_end - knn_start)
    return results

def benchmark_all():
    answer = {
        "Build": {},
        "Data Insertion": {},
        "Key lookup": {},
        "Node Join": {},
        "Node Leave": {},
        "Range Query": {},
        "kNN Query": {}
    }
    i = 50
    while i <= 300:
        print(f"Benchmarking {i} nodes...")
        answer = benchmark(i, answer)
        i += 50
    return answer

def results_print(results: dict) -> None:
    for process in results.items():
        print(f"\n{process[0]} times:")
        for node_count, time in process[1].items():
            print(f"{process[0]} time for {node_count} nodes: {time}")

results_print(benchmark_all())