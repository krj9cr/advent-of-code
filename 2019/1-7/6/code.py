import networkx as nx

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseFile(path: str):
    with open(path, 'r') as file:
        return parseInput(file)

def parseInput(lines):
    return [parseLine(line) for line in lines]

def parseLine(line: str):
    return line.strip().split(")")

###########################
# part1
###########################
def part1(data):
    graph = nx.DiGraph()
    for pair in data:
        graph.add_edge(pair[0], pair[1])
    root = list(nx.topological_sort(graph))[0]
    nodes = set(graph.nodes)
    nodes.remove(root)

    count = 0
    for node in nodes:
        orbits = set()
        for path in nx.all_simple_paths(graph,root,node):
            [orbits.add(p) for p in set(path)]
        orbits.remove(node)
        count += len(orbits)
    print(count)

def testpart1(data):
    lines = parseInput(data)
    part1(lines)

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):
    graph = nx.Graph()
    for pair in data:
        graph.add_edge(pair[0], pair[1])
    print(nx.shortest_path_length(graph, 'YOU', 'SAN')-2)

def testpart2(data):
    lines = parseInput(data)
    part2(lines)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':
    # print("PART 1 TEST DATA")
    # testpart1(["COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L"])

    # print("\nPART 1 RESULT")
    # runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2(["COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L","K)YOU","I)SAN"])

    print("\nPART 2 RESULT")
    runpart2()
