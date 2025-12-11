import sys
import time, os
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


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

def plotGraph(G):
    # Compute positions using graphviz_layout with the 'dot' program
    # 'dot' is the standard for hierarchical/layered layouts
    dot_args = (
        '-Gnodesep=5 '  # Increase horizontal separation (default is 0.5)
        '-Granksep=15 '  # Increase vertical separation (default is 0.5 for 'dot')
        '-Esplines=ortho'  # Use orthogonal (right-angled) edges
    )
    try:
        pos = graphviz_layout(G, prog='dot', args=dot_args)
    except nx.NetworkXException as e:
        print(f"Error with graphviz_layout: {e}. Ensure Graphviz is installed and accessible.")
        # Fallback to a different layout if graphviz fails, though it won't be strictly hierarchical
        pos = nx.spring_layout(G, seed=42)

    # Set up plot
    plt.figure(figsize=(50, 50))  # Increased figure size to accommodate spacing
    node_colors = []
    for node in G.nodes():
        if node in ['svr', 'out', 'fft', 'dac']:
            node_colors.append('red')
        else:
            node_colors.append('lightblue')
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # Display the plot
    plt.axis('off')  # Hide the axis
    plt.show()


def find_all_paths(graph,  nodes_after_fft, nodes_after_dac, start, end, path=[]):
    # Append the current node to the path
    path = path + [start]

    # Base case: If the start node is the end node, we've found a path
    if start == end:
        return [path]

    # If the start node is not in the graph, there are no paths
    if start not in graph:
        print("UH OH", start, "not in graph")
        sys.exit(1)

    paths = []
    # Recurse through all neighbors of the current node
    for node in graph[start]:
        if node in nodes_after_fft and 'fft' not in path:
            continue
        if node in nodes_after_dac and 'dac' not in path:
            continue
        # Find all paths from the neighbor to the end
        newpaths = find_all_paths(graph,  nodes_after_fft, nodes_after_dac, node, end, path)
        # Add the new paths to the main list of paths
        for newpath in newpaths:
            paths.append(newpath)
            print("found path", newpath)

    return paths

def part2():
    conns = parseInput()
    print(conns)

    edges = []
    nodes = set()
    for c in conns:
        nodes.add(c)
        for node in conns[c]:
            edges.append([c, node])
            nodes.add(node)
    print(edges)


    # Create a directed graph
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # plotGraph(G)

    # topo sort
    sorted_nodes = list(nx.topological_sort(G))
    print("Topologically sorted order:", sorted_nodes)
    fft_idx = sorted_nodes.index('fft')
    dac_idx = sorted_nodes.index('dac')
    nodes_after_fft = sorted_nodes[fft_idx+1:]
    nodes_after_dac = sorted_nodes[dac_idx+1:]

    # idea:
    # do dfs?
    # can stop checking paths where we passed fft or dac
    # also seems like in my case, fft is before dac

    # Find all paths and print the result
    all_paths = find_all_paths(conns, nodes_after_fft, nodes_after_dac, 'svr', 'out')
    # for p in all_paths:
    #     print(p)
    print("num paths:", len(all_paths))


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
