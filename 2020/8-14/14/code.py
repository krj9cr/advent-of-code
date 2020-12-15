import time
from copy import deepcopy

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    return line.strip().split(" = ")

mem = {}

# convert int to array of bits
def bitfield(n, numbits):
    a = [1 if digit=='1' else 0 for digit in bin(n)[2:]]
    return ([0] * (numbits - len(a))) + a

# apply bit mask to bit array
# assumes they are the same length
def applyBitmask(bitmask, bitarr):
    res = []
    for i in range(len(bitmask)):
        m = bitmask[i]
        b = bitarr[i]
        if m == "X":
            res.append(b)
        else:
            res.append(int(m))
    return res

def shifting(bitlist):
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit
    return out

def processLine(mask, line):
    cmd = line[0]
    val = line[1]
    if cmd == "mask":
        mask = val
    elif "mem" in cmd:
        memloc = int(cmd.replace("mem[", "").replace("]", ""))
        val = int(val)
        valbits = bitfield(val, len(mask))
        print(''.join([str(i) for i in valbits]))
        print(mask)
        valmasked = applyBitmask(mask, valbits)
        print(''.join([str(i) for i in valmasked]))
        valint = shifting(valmasked)
        mem[memloc] = valint
    return mask


###########################
# part1
###########################
def part1(data):
    print(data)
    numbits = 36
    mask = "X" * 36

    # proess each line
    for line in data:
        mask = processLine(mask, line)
        print(mem)
        print()

    # result
    prod = 0
    for memloc in mem:
        val = mem[memloc]
        prod += val
    print("DONE", prod)

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def applyBitmask2(bitmask, bitarr):
    res = []
    for i in range(len(bitmask)):
        m = bitmask[i]
        b = bitarr[i]
        if m == "0":
            res.append(b)
        elif m == "1":
            res.append(1)
        elif m == "X":
            res.append("X")
        else:
            print("BADNESS")
            return
    return res

def generateAddresses(bitarr):
    if "X" not in bitarr:
        return [bitarr]
    for i in range(len(bitarr)):
        b = bitarr[i]
        if b == "X":
            newbitarr = deepcopy(bitarr)
            newbitarr[i] = 0
            newbitarr2 = deepcopy(bitarr)
            newbitarr2[i] = 1
            return generateAddresses(newbitarr) + generateAddresses(newbitarr2)

def processLine2(mask, line):
    cmd = line[0]
    val = line[1]
    if cmd == "mask":
        mask = val
    elif "mem" in cmd:
        memloc = int(cmd.replace("mem[", "").replace("]", ""))
        val = int(val)
        valbits = bitfield(val, len(mask))
        print(''.join([str(i) for i in valbits]))
        print(mask)
        valmasked = applyBitmask(mask, valbits)
        print(''.join([str(i) for i in valmasked]))
        valint = shifting(valmasked)
        # mask memory, too
        memlocmasked = applyBitmask2(mask, bitfield(memloc, len(mask)))
        addrmasks = generateAddresses(memlocmasked)
        for bitaddr in addrmasks:
            addr = shifting(bitaddr)
            mem[addr] = val
    return mask

def part2(data):
    print(data)
    mask = "X" * 36

    # proess each line
    for line in data:
        mask = processLine2(mask, line)
        # print(mem)
        print()

    # result
    prod = 0
    for memloc in mem:
        val = mem[memloc]
        prod += val
    print("DONE", prod)

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()

