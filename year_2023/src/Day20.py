import time
from abc import ABC, abstractmethod
from enum import Enum

class PulseType(Enum):
    LOW = 0
    HIGH = 1

class Pulse:
    def __init__(self, pulse_type: PulseType, source_module: str, destination_module: str):
        self.pulse_type = pulse_type
        self.source_module = source_module
        self.destination_module = destination_module

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
        super().__init__("button", ["broadcaster"])

    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        return [Pulse(PulseType.LOW, self.name, "broadcaster")]

# Flip-flop modules (prefix %) are either on or off; they are initially off.
class FlipFlop(Module):
    def __init__(self, name: str, destination_modules: list[str]):
        super().__init__(name, destination_modules)
        self.state = 0  # 0 for off, 1 for on

    def __str__(self):
        return "%" + self.name + " -> " + str(self.destination_modules) + "; state: " + str(self.state)

    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
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

# Conjunction modules (prefix &) remember the type of the most recent pulse received from
# each of their connected input modules
class Conjunction(Module):
    def __init__(self, name: str, destination_modules: list[str]):
        super().__init__(name, destination_modules)
        self.memory = {}
        # initially default to remembering a low pulse for each input
        for d in destination_modules:
            self.memory[d] = PulseType.LOW

    def __str__(self):
        return "&" + self.name + " -> " + str(self.destination_modules) + "; memory: " + str(self.memory)

    def process_pulse(self, pulse: Pulse) -> list[Pulse]:
        # first updates its memory for that input
        self.memory[pulse.source_module] = pulse.pulse_type

        # check if all pulses in memory are high
        all_high = True
        for module_name in self.memory:
            if self.memory[module_name] != PulseType.HIGH:
                all_high = False
                break
        # if it remembers high pulses for all inputs, it sends a low pulse
        if all_high:
            [Pulse(PulseType.LOW, self.name, d) for d in self.destination_modules]
        # otherwise, it sends a high pulse
        else:
            return [Pulse(PulseType.HIGH, self.name, d) for d in self.destination_modules]

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        modules = {}
        for line in file:
            line = line.strip().split(" -> ")
            module_name = line[0]
            destination_modules = line[1].split(", ")
            module = None
            if module_name == "broadcaster":
                module = Broadcaster(module_name, destination_modules)
            elif "%" in module_name:
                module_name = module_name.strip("%")
                module = FlipFlop(module_name, destination_modules)
            elif "&" in module_name:
                module_name = module_name.strip("&")
                module = Conjunction(module_name, destination_modules)
            modules[module_name] = module
        return modules

def part1():
    modules = parseInput(20)
    for module_name in modules:
        print(modules[module_name])



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
