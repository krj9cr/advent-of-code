import copy
import sys
import time
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        paths = set()
        forest = set()
        slopes = {}
        j = 0
        for line in file:
            line = line.strip()
            for i in range(len(line)):
                char = line[i]
                if char == ".":
                    paths.add((i, j))
                elif char == "#":
                    forest.add((i, j))
                else:
                    slopes[(i, j)] = char
            j += 1
        return paths, forest, slopes, i + 1, j

def print_grid(paths, forest, slopes, w, h):
    for j in range(h):
        for i in range(w):
            if (i, j) in paths:
                print(".", end="")
            elif (i, j) in forest:
                print("#", end="")
            elif (i, j) in slopes:
                char = slopes[(i, j)]
                print(char, end="")
        print()

neighbor_cache = {}

def get_neighbors(x, y, forest, slopes, w, h, slippery_slopes=True):
    if (x, y) in neighbor_cache:
        return neighbor_cache[(x, y)]
    neighbors = []
    # check if our current spot is a slope
    # apparently the input only contains ">" and "v" slopes, no "^" or "<"
    # we also just assume all slopes correctly contain an open path spot next to them
    if slippery_slopes and (x, y) in slopes:
        char = slopes[(x, y)]
        if char == ">":
            neighbors.append((x + 1, y))
        elif char == "v":
            neighbors.append((x, y + 1))
        else:
            print("UH OH")
            sys.exit(1)
    else:
        for x2, y2 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            # check bounds
            if 0 <= x2 < w and 0 <= y2 < h:
                # check if not forest
                if (x2, y2) not in forest:
                    neighbors.append((x2, y2))
    neighbor_cache[(x, y)] = neighbors
    return neighbors

maxHike = 0

def dfs(hike, x, y, endPos, forest, slopes, w, h, slippery_slopes=True):
    global maxHike
    # check if done
    if (x, y) == endPos:
        # hikes.append(hike)
        dist = len(hike)
        if dist > maxHike:
            maxHike = dist
            print("maxHike", maxHike)
        return

    # TODO: idea: break things into segments? only make decisions at crossroads?
    hike2 = hike + [(x, y)]
    # try each valid neighbor
    for (x2, y2) in get_neighbors(x, y, forest, slopes, w, h, slippery_slopes):
        num_neighbors = len(get_neighbors(x2, y2, forest, slopes, w, h, slippery_slopes))
        if num_neighbors == 1:  # just go for it
            dfs(hike2, x2, y2, endPos, forest, slopes, w, h, slippery_slopes)
        elif num_neighbors > 1:
            if (x2, y2) not in hike:
                dfs(hike2, x2, y2, endPos, forest, slopes, w, h, slippery_slopes)

    # if we get here, the path got stuck? so doing nothing is fine
    # print("stuck on hike:", hike)
    dist = len(hike)
    if dist > maxHike:
        maxHike = dist
        print("maxHike", maxHike)

def part1():
    sys.setrecursionlimit(5000)

    paths, forest, slopes, w, h = parseInput(23)
    startPos = (1, 0)
    endPos = (w - 2, h - 1)
    # print(paths)
    # print(forest)
    # print(slopes)
    # print(w, h)
    # print(startPos, endPos)
    # print()
    # print_grid(paths, forest, slopes, w, h)

    dfs([], startPos[0], startPos[1], endPos, forest, slopes, w, h)
    # max_hike = 0
    # for hike in hikes:
    #     dist = len(hike)
    #     # print(dist, hike)
    #     if dist > max_hike:
    #         max_hike = dist
    # print("max hike:", max_hike)


def find_crossroads(forest, w, h):
    crossroads = set()
    for y in range(h):
        for x in range(w):
            if (x, y) not in forest:
                n = get_neighbors(x, y, forest, {}, w, h, slippery_slopes=False)
                if len(n) >= 3:
                    crossroads.add((x, y))
    return crossroads

# just find th distance between a crossroad and until we arrive at another crossroad
def bfs_to_crossroad(x, y, crossroads, forest, w, h, startPos=None):
    queue = deque([[(x, y)]])
    seen = {(x, y)}
    if startPos:
        seen.add(startPos)
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) in crossroads:
            return (x, y), len(path)
        neighbors = get_neighbors(x, y, forest, {}, w, h, slippery_slopes=False)
        for nextPos in neighbors:
            if nextPos not in seen:
                queue.append(path + [nextPos])
                seen.add(nextPos)

def part2():
    sys.setrecursionlimit(10000)

    paths, forest, slopes, w, h = parseInput(23)
    startPos = (1, 0)
    endPos = (w - 2, h - 1)
    # endPos = (135, 147)  # change this to be the last crossroad
    # print(paths)
    # print(forest)
    # print(slopes)
    # print(w, h)
    print(startPos, endPos)
    # print()
    # print_grid(paths, forest, slopes, w, h)

    # dfs([], startPos[0], startPos[1], endPos, forest, slopes, w, h, slippery_slopes=False)

    # idea: just look at crossroads and start/end points
    # find each crossroad in the grid (spots that have at least 3 neighbors without slippery slopes)
    crossroads = find_crossroads(forest, w, h).union({startPos, endPos})
    print(sorted(list(crossroads)))
    print()
    # find the distance between each crossroad and its... "adjacent" crossroads
    # for each crossroad, go in each direction and do bfs to get distances
    crossroad_distances = {}
    for crossroad in crossroads:
        dists = {}
        x, y = crossroad[0], crossroad[1]
        # print("checking crossroad", crossroad)
        for (x2, y2) in get_neighbors(x, y, forest, {}, w, h, slippery_slopes=False):
            # print("going to neighbor", x2, y2)
            (x3, y3), d = bfs_to_crossroad(x2, y2, crossroads, forest, w, h, (x, y))
            dists[(x3, y3)] = d
        # print(crossroad, dists)
        crossroad_distances[crossroad] = dists
    print(crossroad_distances)

    # construct a graph with weights instead of a grid?
    G = nx.Graph()
    for crossroad in crossroad_distances:
        distances = crossroad_distances[crossroad]
        G.add_node(crossroad, name=str(crossroad))
        for crossroad2 in distances:
            distance = distances[crossroad2]
            G.add_edge(crossroad, crossroad2, weight=distance)

    # draw graph
    # pos = nx.spring_layout(G)  # pos = nx.nx_agraph.graphviz_layout(G)
    # nx.draw(G, pos, with_labels=True)
    # labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    # plt.draw()
    # plt.show()

    # find all paths and then add up weights
    max_weight = 0
    # set our end point as the last crossroad, since we're either done or will go the wrong way there
    for path in nx.all_simple_paths(G, source=startPos, target=(135, 137)):
        # print(path)
        p = path[0]
        total_weight = 0
        for i in range(1, len(path)):
            p2 = path[i]
            # print("at", p, " checking weight", p2)
            weight = crossroad_distances[p][p2]
            total_weight += weight
            p = p2
        if total_weight > max_weight:
            max_weight = total_weight
            print(max_weight)
    print(max_weight)
    # then need to add the last weight to the answer

# 5966 too low
# 6500 too low
# 9460 max as that's how many paths/slopes there are

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
