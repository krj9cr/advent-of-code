from copy import deepcopy
from lib.intcode import Intcode

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [ int(num) for num in [ line.split(",") for line in file ][0] ]

def parseInput(lines):
    return [ int(line) for line in str(lines).split(",") ]

def parseLine(line: str):
    return line.strip()

###########################
# part1
###########################
def part1(data):
    print(data)
    num_computers = 50
    packets = []

    # initialize inputs
    inputs = []
    for i in range(num_computers):
        inputs.append([i])

    def intcoder_callback(inpi, address):
        if inpi == 0:
            return address
        # check if there is a packet for it
        for packet in packets:
            if packet[0] == address:
                if packet[3] == 0:
                    packet[3] = 1
                    return packet[1]
                else:
                    val = packet[2]
                    packets.remove(packet)
                    return val
        return -1

    # initialize intcoders
    intcoders = []
    for i in range(num_computers):
        intcoders.append(Intcode(deepcopy(data), intcoder_callback, address=i))

    # packet queue
    while True:
        # check outputs
        for intcoder in intcoders:
            if len(intcoder.output) == 3:
                o = intcoder.output
                o.append(0)
                packets.append(o)
                intcoder.output = []
            intcoder.step()
        # check packets for end condition
        for packet in packets:
            if packet[0] == 255:
                print("answer",packet[2])
                exit(0)


def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):
    print(data)
    num_computers = 50
    packets = []
    nat = []
    natdelivered = []
    idlecount = 0

    # initialize inputs
    inputs = []
    for i in range(num_computers):
        inputs.append([i])

    def intcoder_callback(inpi, address):
        if inpi == 0:
            return address
        # check if there is a packet for it
        for packet in packets:
            if packet[0] == address:
                if packet[3] == 0:
                    packet[3] = 1
                    return packet[1]
                else:
                    val = packet[2]
                    packets.remove(packet)
                    return val
        return -1

    # initialize intcoders
    intcoders = []
    for i in range(num_computers):
        intcoders.append(Intcode(deepcopy(data), intcoder_callback, address=i))

    # packet queue
    while True:
        # check outputs
        for intcoder in intcoders:
            if len(intcoder.output) == 3:
                o = intcoder.output
                o.append(0)
                if o[0] == 255:
                    nat = deepcopy(o)
                else:
                    packets.append(o)
                intcoder.output = []
            intcoder.step()

        # check for idleness
        if len(packets) == 0:
            idlecount += 1
        if idlecount >= 2000:
            idlecount = 0
            # send last nat packet to address 0
            packet = deepcopy(nat)
            packet[0] = 0
            packets.append(packet)

            # check if we've sent this Y before
            if len(natdelivered) > 0 and packet[2] == natdelivered[-1]:
                print(natdelivered)
                print("answer", packet[2])
                exit(0)
            else:
                natdelivered.append(packet[2])

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()

    print("\nPART 2 RESULT")
    runpart2()
