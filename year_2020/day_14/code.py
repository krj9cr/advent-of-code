import time

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    l = line.strip().split(" = ")
    cmd = l[0]
    val = l[1]
    if cmd == "mask":
        return cmd, val
    elif "mem" in cmd:
        memloc = int(cmd.replace("mem[", "").replace("]", ""))
        val = int(val)
        return "mem", memloc, val

mem = {}

# convert int to array of bits
def bitfield(n, numbits):
    a = "{0:b}".format(n)
    return ("0" * (numbits - len(a))) + a

# apply bit mask to bit array
# assumes they are the same length
def applyBitmask(bitmask, bitstr):
    res = ""
    for i in range(len(bitmask)):
        m = bitmask[i]
        b = bitstr[i]
        if m == "X":
            res += (b)
        else:
            res += (m)
    return res

def shifting(bitstr):
    return int(bitstr, 2)

def processLine(mask, line):
    cmd = line[0]
    val = line[1]
    if cmd == "mask":
        mask = val
    elif cmd == "mem":
        memloc = line[1]
        val = line[2]
        valbits = bitfield(val, len(mask))
        # print(''.join([str(i) for i in valbits]))
        # print(mask)
        valmasked = applyBitmask(mask, valbits)
        # print(''.join([str(i) for i in valmasked]))
        valint = shifting(valmasked)
        mem[memloc] = valint
    return mask


###########################
# part1
###########################
def part1(data):
    # print(data)
    mask = "X" * 36

    # proess each line
    for line in data:
        mask = processLine(mask, line)
        # print(mem)
        # print()

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
    res = ""
    for i in range(len(bitmask)):
        m = bitmask[i]
        b = bitarr[i]
        if m == "0":
            res += b
        elif m == "1":
            res += "1"
        elif m == "X":
            res += "X"
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
            # newbitarr = bitarr[:]
            # newbitarr[i] = 0
            newbitarr = bitarr[:i] + ["0"] + bitarr[i+1:]
            newbitarr2 = bitarr[:i] + ["1"] + bitarr[i+1:]
            # newbitarr2 = bitarr[:]
            # newbitarr2[i] = 1
            return generateAddresses(newbitarr) + generateAddresses(newbitarr2)

def processLine2(mask, line):
    cmd = line[0]
    val = line[1]
    if cmd == "mask":
        mask = val
    elif cmd == "mem":
        memloc = line[1]
        val = line[2]
        valbits = bitfield(val, len(mask))
        # print(''.join([str(i) for i in valbits]))
        # print(mask)
        valmasked = applyBitmask(mask, valbits)
        # print(''.join([str(i) for i in valmasked]))
        valint = shifting(valmasked)
        # mask memory, too
        memlocmasked = applyBitmask2(mask, bitfield(memloc, len(mask)))
        addrmasks = generateAddresses([c for c in memlocmasked])
        for bitaddr in addrmasks:
            addr = shifting("".join([str(b) for b in bitaddr]))
            mem[addr] = val
    return mask

def part2(data):
    # print(data)
    mask = "X" * 36

    # proess each line
    for line in data:
        mask = processLine2(mask, line)
        # print(mem)
        # print()

    # result
    res = 0
    for memloc in mem:
        res += mem[memloc]
    print("DONE", res)

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()

    mem = {}

    print("\nPART 2 RESULT")
    runpart2()
