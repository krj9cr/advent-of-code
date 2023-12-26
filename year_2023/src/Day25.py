import time
import networkx as nx
import matplotlib.pyplot as plt
import itertools


def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        edges = {}
        for line in file:
            line = line.strip().split(": ")
            edges[line[0]] = line[1].split(" ")
        return edges

# https://stackoverflow.com/questions/21739569/finding-separate-graphs-within-a-graph-object-in-networkx
def part1():
    edges = parseInput(25)
    # print(edges)
    pairs = []  # keep track of pairs of edges to try removing
    graph = nx.DiGraph()
    for node in edges:
        connections = edges[node]
        for connection in connections:
            graph.add_edge(node, connection)
            pairs.append((node, connection))
    # print("num pairs", len(pairs))
    # convert to an undirected graph
    UG = graph.to_undirected()

    # find "bridges", sort them by "span"
    # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bridges.local_bridges.html#networkx.algorithms.bridges.local_bridges
    local_bridges = sorted(list(nx.local_bridges(UG)), key=lambda x: x[2], reverse=True)
    # print(len(local_bridges), local_bridges)

    # take the first handful of bridges and remove the "span"
    bridges_to_try = []
    for (a, b, _) in local_bridges[:10]:
        bridges_to_try.append((a, b))
    # print(len(bridges_to_try), bridges_to_try)

    # try removing different combinations of edges
    i = 0
    for comb in itertools.combinations(bridges_to_try, 3):
        # print(i, comb)
        # make an undirected copy of the digraph
        UG = graph.to_undirected()
        for a, b in comb:
            UG.remove_edge(a, b)

        # check for subgraphs - https://stackoverflow.com/a/21751571
        sub_graphs = nx.connected_components(UG)

        answer = 1
        count = 0
        # sub_graphs is a weird generated thing, so enumerating helps deal with it :shrug:
        for i, s in enumerate(sub_graphs):
            size = len(s)
            # print(size, s)
            answer *= size
            count += 1
        if count == 2:
            print("answer", answer)
            break
        print()
        i += 1

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
