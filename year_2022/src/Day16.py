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


# def get_release_for_minute(valves):
#     total = 0
#     for valve_name in valves:
#         valve = valves[valve_name]
#         if valve.is_open:
#             total += valve.flow_rate
#     return total

def get_release_for_minute(open_valves, alphabetical_valve_names, valves):
    total = 0
    for i in range(len(alphabetical_valve_names)):
        is_open = True if open_valves[i] == "1" else False
        if is_open:
            valve_name = alphabetical_valve_names[i]
            valve = valves[valve_name]
            total += valve.flow_rate
    return total

def dfs(state: State, cache):
    cache_key, release_for_minute, opened_valve_names = state.generate_cache_key()
    next_release = state.total_release + release_for_minute

    if state.minutes == 0:
        return state.total_release # next_release
    if cache_key in cache:
        return cache[cache_key]

    current_valve = state.valves[state.current_valve_name]
    # print(" " * depth, "at ", current_valve_name)
    # path 1 is open this valve
    # print("current valve", current_valve)
    answer = 0
    # open the valve
    if current_valve.flow_rate > 0 and not current_valve.is_open:
        new_valves = copy.deepcopy(state.valves)
        current_valve_copy = copy.deepcopy(current_valve)
        # print("opening", state.current_valve_name)
        current_valve_copy.is_open = True
        new_valves[state.current_valve_name] = current_valve_copy
        # minutes -= 1 # it takes 1 extra min to open
        path1 = dfs(State(new_valves, state.current_valve_name, next_release, state.minutes-1), cache)
        answer = max(answer, path1)

    # path 2 is to move
    for tunnel in current_valve.leads_to:
        new_valves = copy.deepcopy(state.valves)
        # print(state.current_valve_name, "following ", tunnel)
        path2 = dfs(State(new_valves, tunnel, next_release, state.minutes-1), cache)
        answer = max(answer, path2)
    # print(" " * depth,"options", options)

    # only cache when at least one valve is open, to avoid the case where we have a bunch of 0 flow_rates in a row
    # if opened_valve_names != "":
        # cache_key, release_for_minute, opened_valve_names = state.generate_cache_key()
    cache[cache_key] = answer
    print("saving ", cache_key, answer)
    # print(cache)
    return answer

def part1():
    valves = parseInput(16)
    print(valves)

    print(dfs(State(valves), {}))

    # pressure = 0
    # minute = 0
    # alphabetical_valve_names = sorted(valves.keys())
    # open_valves = '0' * len(alphabetical_valve_names)
    #
    # options = PriorityQueue()
    # options.put(('AA', open_valves, pressure, minute), 0)
    #
    # best = 0
    # cache = {}
    # # move our location(s)
    # while not options.empty():
    #     # TODO: instead of passing along "valves", we just need to track open valves, which can be a string of binary numbers
    #     # indexed on the alphabetical order of the valves
    #
    #     # TODO: create a cache
    #
    #     # TODO: theoretical cap, if we opened all the valves over the remaining minutes, and it's still worse
    #     # than our best so far, we can stop
    #     (current_valve_name, open_valves, pressure, minute) = options.get()
    #     current_valve = valves[current_valve_name]
    #     hash_key = f"{current_valve_name}:{open_valves}:{pressure}:{minute}"
    #
    #     # if hash_key in cache:
    #     #     cache[hash_key] = pressure
    #     # else:
    #     #     cache[hash_key] = pressure
    #
    #     if minute >= 30:
    #         best = max(best, pressure)
    #         print("hit time, pressure", pressure, "best", best)
    #         continue
    #
    #     # get current pressure
    #     turn_pressure = get_release_for_minute(open_valves, alphabetical_valve_names, valves)
    #     next_pressure = pressure + turn_pressure
    #     next_minute = minute + 1
    #
    #     # open valve if not open, and it's not 0
    #     valve_idx = alphabetical_valve_names.index(current_valve_name)
    #     current_valve_is_open = True if open_valves[valve_idx] == "1" else False
    #     if current_valve.flow_rate > 0 and not current_valve_is_open:
    #         next_valve = current_valve_name
    #         next_open_valves = ""
    #         for i in range(len(open_valves)):
    #             if i == valve_idx:
    #                 next_open_valves += "1"
    #             else:
    #                 next_open_valves += open_valves[i]
    #         # we prioritize by negative pressure, since want max pressure
    #         options.put((next_valve, next_open_valves, next_pressure, next_minute), -next_pressure)
    #
    #     # move to each valve
    #     for tunnel in current_valve.leads_to:
    #         next_valve = tunnel
    #         # we prioritize by negative pressure, since want max pressure
    #         options.put((next_valve, open_valves, next_pressure, next_minute), -next_pressure)
    #     # print(options)
    # print(best)


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
