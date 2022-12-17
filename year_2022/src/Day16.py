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
        self.current_valve_name = current_valve_name
        self.total_release = total_release
        self.minutes = minutes
        if cache is not None:
            self.cache = cache
        else:
            self.cache = {}

    def generate_cache_key(self):
        release_for_minute, opened_valve_names = self.get_release_for_minute()
        return self.current_valve_name + ":" + opened_valve_names + ":" + str(self.total_release)

    def get_release_for_minute(self):
        total = 0
        open_valves = []
        for valve in self.valves.values():
            if valve.is_open:
                total += valve.flow_rate
                open_valves.append(valve.name)
        return total, ",".join(sorted(open_valves))


def dfs(state: State, cache):
    release_for_minute, opened_valve_names = state.get_release_for_minute()
    next_release = state.total_release + release_for_minute

    if state.minutes == 0:
        return state.total_release # next_release
    cache_key = state.generate_cache_key()
    if cache.get(cache_key) is not None:
        return cache[cache_key]

    new_valves = copy.deepcopy(state.valves)
    current_valve = state.valves[state.current_valve_name]
    # print(" " * depth, "at ", current_valve_name)
    # path 1 is open this valve
    # print("current valve", current_valve)
    path1 = 0
    if current_valve.flow_rate > 0:
        if not current_valve.is_open:
            # print(" " * depth,"opening", current_valve_name)
            current_valve.is_open = True
            new_valves[state.current_valve_name] = current_valve
            # minutes -= 1 # it takes 1 extra min to open
        path1 = dfs(State(new_valves, state.current_valve_name, next_release, state.minutes-1), cache)

    # path 2 is to move
    options = []
    for tunnel in current_valve.leads_to:
        # print(" " * depth,"following ", tunnel)
        path2 = dfs(State(state.valves, tunnel, next_release, state.minutes-1), cache)
        options.append(path2)
    # print(" " * depth,"options", options)

    answer = max(path1, max(options))
    cache[cache_key] = answer
    print("saving ", cache_key, answer)
    # print(cache)
    return answer

def part1():
    valves = parseInput(16)
    # print(valves)


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
