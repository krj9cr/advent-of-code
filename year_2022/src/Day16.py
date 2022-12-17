import copy
import heapq
import time

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
        return f"Valve {self.name} has flow rate = {self.flow_rate}; tunnels to: {self.leads_to}"

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

class State:
    def __init__(self, valves, current_valve_name='AA', total_release=0, minutes=30, cache=None):
        self.valves = valves
        self.sorted_valve_names = []
        for valve in self.valves.values():
            self.sorted_valve_names.append(valve.name)
        self.sorted_valve_names = sorted(self.sorted_valve_names)
        self.current_valve_name = current_valve_name
        self.total_release = total_release
        self.minutes = minutes
        if cache is not None:
            self.cache = cache
        else:
            self.cache = {}

    def generate_cache_key(self):
        release_for_minute, opened_valve_names = self.get_release_for_minute()
        return self.current_valve_name + ":" + opened_valve_names + ":" + str(self.total_release), release_for_minute, opened_valve_names


    def get_release_for_minute(self):
        total = 0
        open_valves = []
        for valve_name in self.sorted_valve_names:
            valve = self.valves[valve_name]
            if valve.is_open:
                total += valve.flow_rate
                open_valves.append(valve.name)
            # else:
            #     open_valves.append('0')
        return total, ",".join(open_valves)


def dfs(state: State, cache):
    cache_key, release_for_minute, opened_valve_names = state.generate_cache_key()
    next_release = state.total_release + release_for_minute

    if state.minutes == 0:
        return state.total_release # next_release
    if cache.get(cache_key) is not None:
        return cache[cache_key]

    new_valves = copy.deepcopy(state.valves)
    current_valve = state.valves[state.current_valve_name]
    current_valve_copy = copy.deepcopy(current_valve)
    # print(" " * depth, "at ", current_valve_name)
    # path 1 is open this valve
    # print("current valve", current_valve)
    path1 = 0
    # open the valve
    if current_valve.flow_rate > 0 and not current_valve.is_open:
        # print("opening", state.current_valve_name)
        current_valve_copy.is_open = True
        new_valves[state.current_valve_name] = current_valve_copy
        # minutes -= 1 # it takes 1 extra min to open
        path1 = dfs(State(new_valves, state.current_valve_name, next_release, state.minutes-1), cache)
    # don't open the valve
    options = [path1]

    # path 2 is to move
    for tunnel in current_valve.leads_to:
        # print(state.current_valve_name, "following ", tunnel)
        path2 = dfs(State(state.valves, tunnel, next_release, state.minutes-1), cache)
        options.append(path2)
    # print(" " * depth,"options", options)

    answer = max(options)
    # only cache when at least one valve is open, to avoid the case where we have a bunch of 0 flow_rates in a row
    # if opened_valve_names != "":
    cache[cache_key] = answer
    print("saving ", cache_key, answer)
    # print(cache)
    return answer

def part1():
    valves = parseInput(16)
    print(valves)


    print(dfs(State(valves), {}))


def part2():
    lines = parseInput(16)
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
