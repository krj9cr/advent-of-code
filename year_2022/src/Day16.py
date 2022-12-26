import copy
import heapq
import time
import matplotlib.pyplot as plt
import networkx as nx

class Valve:
    def __init__(self, name, flow_rate=0, leads_to=None, is_open=False):
        self.name = name
        if leads_to is None:
            self.leads_to = []
        else:
            self.leads_to = leads_to
        self.flow_rate = flow_rate
        self.is_open = is_open

    def __repr__(self):
        # return f"Valve {self.name} has flow rate = {self.flow_rate}; tunnels to: {self.leads_to}"
        return self.name

    def __lt__(self, other):
        return self.flow_rate > other.flow_rate

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        valves = {}
        for line in lines:
            name = line[6:8]
            split_line = line.split(";")
            rate = int(split_line[0].split("=")[-1])
            # print(name, rate)
            leads_to = [ valve.strip() for valve in split_line[1].strip(" tunnels lead to valves ").split(",")]
            valves[name] = (Valve(name, rate, leads_to))
        return valves


# A custom priority queue used for A Star Search below
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

    def __repr__(self):
        return str(self.elements)

def get_release_for_minute(open_valves, alphabetical_valve_names, valves):
    total = 0
    for i in range(len(alphabetical_valve_names)):
        is_open = True if open_valves[i] == "1" else False
        if is_open:
            valve_name = alphabetical_valve_names[i]
            valve = valves[valve_name]
            total += valve.flow_rate
    return total

def get_unopened_valves(open_valves, alphabetical_valve_names, valves):
    result = []
    for i in range(len(alphabetical_valve_names)):
        is_open = True if open_valves[i] == "1" else False
        valve_name = alphabetical_valve_names[i]
        valve = valves[valve_name]
        if not is_open and valve.flow_rate > 0:
            result.append(valve)
    return result

def part1():
    valves = parseInput(16)
    # print(valves)

    # create a graph to get shortest distance between all pairs of nodes
    valve_edges = {}
    for valve_name in valves:
        valve = valves[valve_name]
        valve_edges[valve_name] = valve.leads_to
    graph = nx.from_dict_of_lists(valve_edges)
    all_pairs_shortest_path = dict(nx.all_pairs_shortest_path(graph))

    # draw the graph
    # nx.draw(
    #     graph,
    #     with_labels=True,
    #     node_size=800,
    #     node_color="#ffff8f",
    #     width=0.8,
    #     font_size=10,
    # )
    # plt.show()

    pressure = 0
    minute = 0
    num_valves_with_flow = 0
    alphabetical_valve_names = []
    for valve_name in valves:
        valve = valves[valve_name]
        if valve.flow_rate > 0:
            num_valves_with_flow += 1
            alphabetical_valve_names.append(valve_name)
    alphabetical_valve_names = sorted(alphabetical_valve_names)
    open_valves = '0' * num_valves_with_flow
    all_open = '1' * num_valves_with_flow

    options = PriorityQueue()
    options.put(('AA', open_valves, pressure, minute), 0)

    best = 0
    # move our location(s)
    while not options.empty():
        (current_valve_name, open_valves, pressure, minute) = options.get()
        current_valve = valves[current_valve_name]
        hash_key = f"{current_valve_name}:{open_valves}:{pressure}:{minute}"

        # get current pressure
        turn_pressure = get_release_for_minute(open_valves, alphabetical_valve_names, valves)

        # if all valves are open, we can just wait until the end
        if open_valves == all_open:
            minutes_left = 30 - minute
            best = max(best, pressure + (turn_pressure * minutes_left))
            # no new states
            continue

        # print("curr", current_valve_name, "pressure", pressure, "considering",  get_unopened_valves(open_valves, alphabetical_valve_names, valves))
        # for every unopened valve > 0, try to move to it
        for valve in get_unopened_valves(open_valves, alphabetical_valve_names, valves):
            cost_to_move_and_open = len(all_pairs_shortest_path[current_valve_name][valve.name])
            # print("cost to move from ", current_valve_name, "to", valve.name, ":", cost_to_move_and_open)
            next_minute = minute + cost_to_move_and_open
            # if moving to and opening the valve exceeds the time limit, just wait it out
            if next_minute >= 30:
                minutes_left = 30 - minute
                best = max(best, pressure + (turn_pressure * minutes_left))
                # no new states
                continue

            # go to it and open, create new states
            next_pressure = pressure + (turn_pressure * cost_to_move_and_open)
            # open it
            next_valve_idx = alphabetical_valve_names.index(valve.name)
            next_open_valves = ""
            for i in range(len(open_valves)):
                if i == next_valve_idx:
                    next_open_valves += "1"
                else:
                    next_open_valves += open_valves[i]
            # we prioritize by negative pressure, since want max pressure
            options.put((valve.name, next_open_valves, next_pressure, next_minute), -next_pressure)

    print(best)


def part2():
    valves = parseInput(16)
    # print(valves)

    # create a graph to get shortest distance between all pairs of nodes
    valve_edges = {}
    for valve_name in valves:
        valve = valves[valve_name]
        valve_edges[valve_name] = valve.leads_to
    graph = nx.from_dict_of_lists(valve_edges)
    all_pairs_shortest_path = dict(nx.all_pairs_shortest_path(graph))

    # draw the graph
    # nx.draw(
    #     graph,
    #     with_labels=True,
    #     node_size=800,
    #     node_color="#ffff8f",
    #     width=0.8,
    #     font_size=10,
    # )
    # plt.show()

    pressure = 0
    minute = 0
    num_valves_with_flow = 0
    alphabetical_valve_names = []
    for valve_name in valves:
        valve = valves[valve_name]
        if valve.flow_rate > 0:
            num_valves_with_flow += 1
            alphabetical_valve_names.append(valve_name)
    alphabetical_valve_names = sorted(alphabetical_valve_names)
    open_valves = '0' * num_valves_with_flow
    all_open = '1' * num_valves_with_flow

    options = PriorityQueue()
    options.put(('AA', open_valves, pressure, minute), 0)

    best = {} # keep track of best for each set of opened valves
    # move our location(s)
    while not options.empty():
        (current_valve_name, open_valves, pressure, minute) = options.get()
        current_valve = valves[current_valve_name]
        hash_key = f"{current_valve_name}:{open_valves}:{pressure}:{minute}"

        # get current pressure
        turn_pressure = get_release_for_minute(open_valves, alphabetical_valve_names, valves)

        minutes_left = 26 - minute
        end_pressure = pressure + (turn_pressure * minutes_left)
        if open_valves in best:
            if end_pressure > best[open_valves]:
                best[open_valves] = end_pressure
        else:
            best[open_valves] = end_pressure

        # if all valves are open, we can just wait until the end
        if open_valves == all_open:
            # no new states
            continue

        # print("curr", current_valve_name, "pressure", pressure, "considering",  get_unopened_valves(open_valves, alphabetical_valve_names, valves))
        # for every unopened valve > 0, try to move to it
        for valve in get_unopened_valves(open_valves, alphabetical_valve_names, valves):
            cost_to_move_and_open = len(all_pairs_shortest_path[current_valve_name][valve.name])
            # print("cost to move from ", current_valve_name, "to", valve.name, ":", cost_to_move_and_open)
            next_minute = minute + cost_to_move_and_open
            # if moving to and opening the valve exceeds the time limit, just wait it out
            if next_minute >= 26:
                # no new states
                continue

            # go to it and open, create new states
            next_pressure = pressure + (turn_pressure * cost_to_move_and_open)
            # open it
            next_valve_idx = alphabetical_valve_names.index(valve.name)
            next_open_valves = ""
            for i in range(len(open_valves)):
                if i == next_valve_idx:
                    next_open_valves += "1"
                else:
                    next_open_valves += open_valves[i]
            # we prioritize by negative pressure, since want max pressure
            options.put((valve.name, next_open_valves, next_pressure, next_minute), -next_pressure)

    # the elephant and us should open different sets of valves to be optimal
    best_combos = 0
    for path1 in best:
        for path2 in best:
            if path1 == path2:
                continue
            disjoint = True
            for i in range(len(path1)):
                if path1[i] == "1" and path2[i] == "1":
                    disjoint = False
                    break
            if disjoint:
                best_combos = max(best_combos, best[path1] + best[path2])

    print(best_combos)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
