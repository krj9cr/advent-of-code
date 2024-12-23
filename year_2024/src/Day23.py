import time
import networkx as nx

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        edges = []
        for line in file:
            line = line.strip().split("-")
            edges.append(line)
        nodes = set([item for sublist in edges for item in sublist])
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        return G, nodes, edges

def starts_with_t(node):
    return node.startswith("t")

def part1():
    G, nodes, edges = parseInput(23)
    print(G)
    t_nodes = list(filter(starts_with_t, nodes))
    print(t_nodes)

    total = 0
    for clique in nx.enumerate_all_cliques(G):
        if len(clique) == 3:
            for node in clique:
                if node in t_nodes:
                    print(clique)
                    total += 1
                    break

    print(total)

def part2():
    lines = parseInput(23)
    print(lines)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    # print("\nPART 2 RESULT")
    # start = time.perf_counter()
    # part2()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)
