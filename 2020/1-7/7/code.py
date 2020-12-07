import networkx as nx
import matplotlib.pyplot as plt

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    s1 =  line.strip().split(" contain ")
    root = s1[0].split(" bags")[0]
    nodes = [ n.replace(" bags", "").replace(" bag", "") for n in s1[1].strip('.').split(', ') ]
    blah = {}
    for n in nodes:
        if n == "no other":
            break
        b = n.split(" ")
        num = int(b[0])
        name = " ".join([ n for n in b[1:] ])

        blah[name] = num
    return root, blah


###########################
# part1
###########################
def part1(data):
    print(data)
    G = nx.DiGraph()

    # add nodes
    for root, nodesmap in data:
        G.add_node(root)
        for item in nodesmap:
            G.add_node(item)
            # add edge
            G.add_edge(root, item, num=nodesmap[item])
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()
    result = 0
    for root, nodesmap in data:
        # print(root)
        p = list(nx.all_simple_paths(G, root, "shiny gold"))
        print(p)
        if len(p) > 0:
            result += 1
    print(result)

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def lookup(bag, d):
    result = 0
    if d.get(bag) is not None:
        result += 1
        nexts = d[bag]
        for item in nexts:
            result += nexts[item] * lookup(item, d)
    return result

def part2(data):
    # print(data)
    biggo = {}
    for root, nodesmap in data:
        biggo[root] = nodesmap
    print(biggo)

    result = lookup("shiny gold", biggo)
    print(result)



    # G = nx.DiGraph()

    # add nodes
    # for root, nodesmap in data:
    #     G.add_node(root)
    #     for item in nodesmap:
    #         G.add_node(item)
    #         # add edge
    #         G.add_edge(root, item, weight=nodesmap[item])
    # e = list(nx.bfs_edges(G, "shiny gold"))
    # print(e)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
