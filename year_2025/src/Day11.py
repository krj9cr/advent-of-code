import time, os
import networkx as nx
import matplotlib.pyplot as plt


def parseInput():
    # Get the day number from the current file
    full_path = __file__
    file_name = os.path.basename(full_path)
    dayf = file_name.strip("Day").strip(".py")

    # Find the input file for this day and read in its lines
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        conns = {}
        for line in file:
            line = line.strip().split(":")
            first = line[0]
            rest = line[1].strip().split(" ")
            conns[first] = rest
        return conns

def part1():
    conns = parseInput()
    print(conns)

    edges = []
    for c in conns:
        for node in conns[c]:
            edges.append([c, node])
    print(edges)


    # Create a directed graph
    DG = nx.DiGraph()
    DG.add_edges_from(edges)

    source_node = 'you'
    target_node = 'out'

    # Find all simple paths (paths without cycles)
    all_paths = list(nx.all_simple_paths(DG, source=source_node, target=target_node))

    print(f"All simple paths from {source_node} to {target_node}:")
    for path in all_paths:
        print(path)
    print(len(all_paths))

def part2():
    conns = parseInput()
    print(conns)

    edges = []
    for c in conns:
        for node in conns[c]:
            edges.append([c, node])
    print(edges)


    # Create a directed graph
    G = nx.DiGraph()
    G.add_edges_from(edges)

    nx.write_graphml(G, "large_graph.graphml")

    # svr = 'svr'
    # out = 'out'
    # dac = 'dac'
    # fft = 'fft'
    #
    # # Find all simple paths (paths without cycles)
    # svr_dac = list(nx.all_simple_paths(G, source=svr, target=dac))
    # dac_fft = list(nx.all_simple_paths(G, source=dac, target=fft))
    # fft_out = list(nx.all_simple_paths(G, source=fft, target=out))
    #
    # print("halfway")
    #
    # svr_fft = list(nx.all_simple_paths(G, source=svr, target=fft))
    # fft_dac = list(nx.all_simple_paths(G, source=fft, target=dac))
    # dac_out = list(nx.all_simple_paths(G, source=dac, target=out))
    #
    # print("some amount of paths)")

if __name__ == "__main__":
    # print("\nPART 1 RESULT")
    # start = time.perf_counter()
    # part1()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
