import interface as iff
from time import perf_counter
import random
from main import KS

HS = 2**KS

def benchmark(NC: int, results: dict) -> dict:
    interface = iff.Interface()

    # Build network with NC nodes
    build_start = perf_counter()
    interface.build_network(NC)
    build_end = perf_counter()

    # Insert all data to the network
    data_start = perf_counter()
    items = iff.parse_csv("NH4_NO3.csv")
    interface.insert_all_data(items.items())
    data_end = perf_counter()

    # Generate random numbers to use for benchmarking
    (leave_n, kNN_n, ex_match_n) = random.sample(sorted(interface.nodes), 3)
    search_key = random.randint(a=0, b=HS-1)
    first_node = interface.get_node()

    for i in range(HS):
        if i not in interface.nodes:
            nn_id = i
            break

    in_key = "2030/05/05_420"
    in_data = "In data"
    up_data = "Update data"
    del_key = random.sample(sorted(items), 1)[0]

    # Start process benchmarking NC Nodes

    # Insert key
    in_key_start = perf_counter()
    interface.insert_item((in_key, in_data), first_node.id)
    in_key_end = perf_counter()

    # Delete key
    del_key_start = perf_counter()
    interface.delete_item(key=del_key, start_node_id=first_node.id)
    del_key_end = perf_counter()

    # Update record based on key
    up_key_start = perf_counter()
    interface.update_record((in_key, up_data), first_node.id)
    up_key_end = perf_counter()

    # Key lookup 
    query_start = perf_counter()
    first_node.find_successor(search_key)
    query_end = perf_counter()

    # Node join
    join_start = perf_counter()
    interface.node_join(new_node_id=nn_id, start_node_id=first_node.id)
    join_end = perf_counter()

    # Node Leave
    leave_start = perf_counter()
    interface.node_leave(leave_n, first_node.id)
    leave_end = perf_counter()

    # Massive nodes' failure
    mnn_start = perf_counter()

    mnn_end = perf_counter()

    # Exact match
    ex_match_start = perf_counter()
    interface.exact_match(key=ex_match_n, start_node_id=first_node.id)
    ex_match_end = perf_counter()

    # Range query
    range_start = perf_counter()
    interface.range_query(150, 250)
    range_end = perf_counter()

    # kNN query
    knn_start = perf_counter()
    interface.knn(5, kNN_n)
    knn_end = perf_counter()


    results['Build'][NC] = (build_end - build_start)
    results['Insert all data'][NC] = (data_end - data_start)
    results['Insert key'][NC] = (in_key_end - in_key_start)
    results['Delete key'][NC] = (del_key_end - del_key_start)
    results['Update key'][NC] = (up_key_end - up_key_start)
    results['Key lookup'][NC] = (query_end - query_start)
    results['Node Join'][NC] = (join_end - join_start)
    results['Node Leave'][NC] = (leave_end - leave_start)
    results['Massive Nodes\' failure'][NC] = (mnn_end - mnn_start)
    results['Exact match'][NC] = (ex_match_end - ex_match_start)
    results['Range Query'][NC] = (range_end - range_start)
    results['kNN Query'][NC] = (knn_end - knn_start)
    return results

def benchmark_all():
    answer = {
        "Build": {},
        "Insert all data": {},
        "Insert key": {},
        "Delete key": {},
        "Update key": {},
        "Key lookup": {},
        "Node Join": {},
        "Node Leave": {},
        "Massive Nodes' failure": {},
        "Exact match": {},
        "Range Query": {},
        "kNN Query": {}
    }
    for i in range(20, 301, 40):
        print(f"Benchmarking {i} nodes...")
        answer = benchmark(i, answer)
    return answer

def results_print(results: dict) -> None:
    for process in results.items():
        print(f"\n{process[0]} times:")
        for node_count, time in process[1].items():
            print(f"{process[0]} time for {node_count} nodes: {time}")

results_print(benchmark_all())