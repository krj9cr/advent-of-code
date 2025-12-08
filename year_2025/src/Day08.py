import math
import time, os
import networkx as nx

def parseInput():
    # Get the day number from the current file
    full_path = __file__
    file_name = os.path.basename(full_path)
    dayf = file_name.strip("Day").strip(".py")

    # Find the input file for this day and read in its lines
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        counter = 0
        for line in file:
            line = tuple([int(i) for i in line.strip().split(',')])
            lines.append((counter, line))
            counter += 1
        return lines

def part1():
    lines = parseInput()
    print(lines)

    # find distances between all pairs?
    distances = {}
    # map "id1->id2" -> distance
    for id1, node1 in lines:
        (x1, y1, z1) = node1
        for id2, node2 in lines:
            if id1 == id2:
                continue
            (x2, y2, z2) = node2
            hash = str(min(id1, id2)) + '->' + str(max(id1, id2))
            if hash in distances:
                continue
            distances[hash] = math.dist(node1, node2)
            print(hash)

    sorted_items = sorted(distances.items(), key=lambda item: item[1])
    print(sorted_items)

    # make top connections
    num_connections = 1000 # 1000
    G = nx.Graph()
    G.add_nodes_from([item[1] for item in lines])
    for n in range(num_connections):
        ids = sorted_items[n][0]
        ids_split = ids.split('->')
        id1 = int(ids_split[0])
        id2 = int(ids_split[1])
        print(id1, id2)
        node1 = lines[id1][1]
        node2 = lines[id2][1]
        print(node1, node2)
        G.add_edge(node1, node2)

    components = list(nx.connected_components(G))
    # print(f"The connected components are: {components}")
    sorted_comps = sorted(components, key=len, reverse=True)
    # print(sorted_comps)

    answer = 1
    for i in range(3):
        print(sorted_comps[i])
        answer *= len(sorted_comps[i])
    print("answer", answer)


def part2():
    lines = parseInput()
    # print(lines)

    # find distances between all pairs?
    distances = {}
    # map "id1->id2" -> distance
    for id1, node1 in lines:
        (x1, y1, z1) = node1
        for id2, node2 in lines:
            if id1 == id2:
                continue
            (x2, y2, z2) = node2
            hash = str(min(id1, id2)) + '->' + str(max(id1, id2))
            if hash in distances:
                continue
            distances[hash] = math.dist(node1, node2)
            # print(hash)

    sorted_items = sorted(distances.items(), key=lambda item: item[1])
    # print(sorted_items)

    # make top connections
    num_connections = 0 # 1000
    G = nx.Graph()
    G.add_nodes_from([item[1] for item in lines])
    while True:
        ids = sorted_items[num_connections][0]
        ids_split = ids.split('->')
        id1 = int(ids_split[0])
        id2 = int(ids_split[1])
        # print(id1, id2)
        node1 = lines[id1][1]
        node2 = lines[id2][1]
        # print(node1, node2)
        G.add_edge(node1, node2)

        # check num connected components
        components = list(nx.connected_components(G))
        if len(components) == 1:
            print("OHO", num_connections)
            print("answwer", node1[0] * node2[0])
            break
        num_connections += 1



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
