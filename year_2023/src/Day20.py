import time
from abc import ABC, abstractmethod
from enum import Enum
import queue

BROADCASTER = "broadcaster"
BUTTON = "button"

class PulseType(Enum):
    LOW = 0
    HIGH = 1

class Pulse:
    def __init__(self, pulse_type: PulseType, source_module: str, destination_module: str):
        self.pulse_type = pulse_type
        self.source_module = source_module
        self.destination_module = destination_module

    def __str__(self):
        pulse_type = "high"
        if self.pulse_type == PulseType.LOW:
            pulse_type = "low"
        return self.source_module + " -" + pulse_type + "-> " + self.destination_module

class Module(ABC):
    def __init__(self, name: str, destination_modules: list[str]):
        self.name = name
        self.destination_modules = destination_modules

    @abstractmethod
    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        pass

    def __str__(self):
        return self.name + " -> " + str(self.destination_modules)

# sends the same pulse to all of its destination modules
class Broadcaster(Module):
    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        return [Pulse(pulse.pulse_type, self.name, d) for d in self.destination_modules]

# sends a single low pulse is sent directly to the broadcaster module
class Button(Module):
    def __init__(self):
        super().__init__(BUTTON, [BROADCASTER])

    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        return [Pulse(PulseType.LOW, self.name, BROADCASTER)]

# Flip-flop modules (prefix %) are either on or off; they are initially off.
class FlipFlop(Module):
    def __init__(self, name: str, destination_modules: list[str]):
        super().__init__(name, destination_modules)
        self.state = 0  # 0 for off, 1 for on

    def __str__(self):
        return "%" + self.name + " -> " + str(self.destination_modules) + "; state: " + str(self.state)

    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        # print("flip flop", self.name, pulse, "state:", self.state)
        # If a flip-flop module receives a high pulse, it is ignored and nothing happens.
        if pulse.pulse_type == PulseType.HIGH:
            return []
        # However, if a flip-flop module receives a low pulse, it flips between on and off.
        # If it was off, it turns on and sends a high pulse.
        if self.state == 0:
            self.state = 1
            return [Pulse(PulseType.HIGH, self.name, d) for d in self.destination_modules]
        # If it was on, it turns off and sends a low pulse.
        else:
            self.state = 0
            return [Pulse(PulseType.LOW, self.name, d) for d in self.destination_modules]

# doesn't do anything
class TestModule(Module):
    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        return []

# Conjunction modules (prefix &) remember the type of the most recent pulse received from
# each of their connected input modules
class Conjunction(Module):
    def __init__(self, name: str, destination_modules: list[str]):
        super().__init__(name, destination_modules)
        self.memory = {}

    def initialize_memory(self, source_module_names):
        # initially default to remembering a low pulse for each input
        for s in source_module_names:
            self.memory[s] = PulseType.LOW

    def __str__(self):
        return "&" + self.name + " -> " + str(self.destination_modules) + "; memory: " + str(self.memory)

    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        # first updates its memory for that input
        # if self.memory.get(pulse.source_module):
        self.memory[pulse.source_module] = pulse.pulse_type

        # check if all pulses in memory are high
        all_high = True
        for module_name in self.memory:
            if self.memory[module_name] != PulseType.HIGH:
                all_high = False
                break
        # if it remembers high pulses for all inputs, it sends a low pulse
        if all_high:
            return [Pulse(PulseType.LOW, self.name, d) for d in self.destination_modules]
        # otherwise, it sends a high pulse
        else:
            return [Pulse(PulseType.HIGH, self.name, d) for d in self.destination_modules]

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        modules = {}
        conjunction_module_names = []
        for line in file:
            line = line.strip().split(" -> ")
            module_name = line[0]
            destination_modules = line[1].split(", ")
            module = None
            if module_name == BROADCASTER:
                module = Broadcaster(module_name, destination_modules)
            elif "%" in module_name:
                module_name = module_name.strip("%")
                module = FlipFlop(module_name, destination_modules)
            elif "&" in module_name:
                module_name = module_name.strip("&")
                module = Conjunction(module_name, destination_modules)
                conjunction_module_names.append(module_name)
            modules[module_name] = module
        # initialize Conjunction modules' memories with their inputs
        for conjunction_module_name in conjunction_module_names:
            module = modules[conjunction_module_name]
            source_module_names = []
            # find all modules that input to it
            for module_name in modules:
                module2 = modules[module_name]
                if conjunction_module_name in module2.destination_modules:
                    source_module_names.append(module_name)
            # initialize
            module.initialize_memory(source_module_names)
        return modules

def part1():
    modules = parseInput(20)
    # for m in modules:
    #     print(modules[m])

    # add TestModules that are coded but don't exist
    modules["output"] = TestModule("output", [])  # example 2
    modules["rx"] = TestModule("rx", [])  # my input

    num_high = num_low = 0

    for i in range(1000):
        pulse_queue = queue.Queue()

        # simulate initial button push
        pulse_queue.put(Pulse(PulseType.LOW, BUTTON, BROADCASTER))

        # keep processing until there's no pulses left
        while not pulse_queue.empty():
            pulse = pulse_queue.get()
            if pulse.pulse_type == PulseType.HIGH:
                num_high += 1
            else:
                num_low +=1
            # print(pulse)
            module = modules[pulse.destination_module]
            sent_pulses = module.process_pulse(pulse)
            for sent_pulse in sent_pulses:
                pulse_queue.put(sent_pulse)
        # print("---")

    # print("high:", num_high, "low:", num_low)
    print("answer:", num_high * num_low)


def part2():
    lines = parseInput(20)
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
