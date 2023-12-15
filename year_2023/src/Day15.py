import time
from collections import OrderedDict

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        line = [line.strip() for line in file][0]
        return line.split(',')

def HASH(string):
    curr = 0
    for char in string:
        ascii_code = ord(char)
        # print("ascii_code", ascii_code)
        curr += ascii_code
        # print("curr", curr)
        curr *= 17
        curr %= 256
    return curr

def part1():
    steps = parseInput(15)
    print(steps)

    answer = 0
    for step in steps:
        print(step)
        answer += HASH(step)
    print(answer)


def part2():
    steps = parseInput(15)
    print(steps)

    # init boxes
    boxes = {}
    for i in range(256):
        boxes[i] = OrderedDict()

    for step in steps:
        if "-" in step:
            label = step.strip("-")
            boxId = HASH(label)
            box = boxes[boxId]
            if label in box:
                del box[label]
        elif "=" in step:
            splitStep = step.split("=")
            label = splitStep[0]
            focalLength = splitStep[1]
            boxId = HASH(label)
            box = boxes[boxId]
            if label in box:
                # replace lens
                box[label] = focalLength
            else:
                box[label] = focalLength
            boxes[boxId] = box
        # # print (for debugging)
        # print(step, "boxId", boxId)
        # for boxId in boxes:
        #     box = boxes[boxId]
        #     if len(box) > 0:
        #         print("Box", boxId, box)

    answer = 0
    for boxId in boxes:
        box = boxes[boxId]
        if len(box) > 0:
            print("Box", boxId, box)
        i = 0
        while i < len(box):
            label = list(box)[i]
            focus = box[label]
            print(label, focus)
            a = (1 + boxId) * (i + 1) * int(focus)
            print((1 + boxId),  (i + 1), int(focus), "=", a)
            answer += a
            i += 1
    print(answer)

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
