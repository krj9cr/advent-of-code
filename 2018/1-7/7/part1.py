from collections import defaultdict
import networkx as nx

# graph problem with topological sort

def parseInput(input):
    pairs = []
    with open(input, 'r') as file:
        for line in file:
            s = line.strip().split(" ")
            first = (s[1])
            second = (s[7])
            pairs.append([first, second])
    return pairs


def solve(lines):
    G = nx.DiGraph()
    for line in lines:
        parts = line.split(" ")
        G.add_edge(parts[1], parts[7])
    print(''.join(nx.lexicographical_topological_sort(G)))


def createGraph(pairs):
    flatpairs = [item for sublist in pairs for item in sublist]
    num_uniq = len(set(flatpairs))
    print("num_uniq:" + str(num_uniq))

    graph = Graph(num_uniq)
    for pair in pairs:
        graph.addEdge(pair[0], pair[1])
    for uniq in flatpairs:
        if graph.graph.get(uniq) is None:
            graph.addEdge(uniq, None)
    return graph


# Class to represent a graph
class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)  # dictionary containing adjacency List
        self.V = vertices  # No. of vertices

    # function to add an edge to graph
    def addEdge(self, u, v):
        if v is None:
            self.graph[u] = []
        else:
            self.graph[u].append(v)
        sorted(self.graph[u])

    # A recursive function used by topologicalSort
    def topologicalSortUtil(self, v, visited, stack):
        # Mark the current node as visited.
        visited.add(v)
        print("  "+v)

        # Recur for all the vertices adjacent to this vertex
        for i in range(0, len(self.graph[v])):
            adjv = self.graph[v][i]
            if adjv not in visited:
                if i == 0:
                    rest = self.graph[v][1:]
                    for r in rest:
                        self.graph[adjv].append(r)
                    sorted(self.graph[adjv])
                self.topologicalSortUtil(adjv, visited, stack)

        # Push current vertex to stack which stores result
        stack.insert(0, v)
        print(self.graph)
        print(stack)

    # The function to do Topological Sort. It uses recursive topologicalSortUtil()
    def topologicalSort(self):
        # Mark all the vertices as not visited
        visited = set()
        stack = []

        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        for v in self.graph:
            print(v)
            if v not in visited:
                self.topologicalSortUtil(v, visited, stack)

        # Print contents of stack
        print(stack)


def part1(filePath):
    with open(filePath, 'r') as file:
        lines = [line for line in file]
        solve(lines)
