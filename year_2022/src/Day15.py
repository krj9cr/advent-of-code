import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        beacons = []
        sensors = []
        for line in lines:
            split = line.split(":")
            for item in split:
                split2 = item.split("=")
                if split2[0].startswith("Sensor"):
                    sensors.append((int(split2[1].split(",")[0]), int(split2[2])))
                else:
                    beacons.append((int(split2[1].split(",")[0]), int(split2[2])))
        return sensors, beacons

def manhattan(one, two):
    return abs(one[0] - two[0]) + abs(one[1] - two[1])

# https://www.geeksforgeeks.org/merging-intervals/
def mergeIntervals(intervals):
    # Sort the array on the basis of start values of intervals.
    intervals.sort()
    stack = [intervals[0]]
    # insert first interval into stack
    for i in intervals[1:]:
        # Check for overlapping interval,
        # if interval overlap
        if stack[-1][0] <= i[0] <= stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], i[-1])
        else:
            stack.append(i)

    # print("The Merged Intervals are :", end=" ")
    # for i in range(len(stack)):
    #     print(stack[i], end=" ")
    return stack

def part1():
    sensors, beacons = parseInput(15)
    print(sensors)
    num_sensors = len(sensors)
    print(beacons)
    # shortest_dists = []
    y = 2000000
    # y = 10
    y_no_beacons = set()
    ranges = []
    for i in range(num_sensors):
        dist = manhattan(sensors[i], beacons[i])
        # shortest_dists.append(dist)
        sensor = sensors[i]

        # check "diamond", but only in row y
        # inspired by: https://stackoverflow.com/questions/64823023/determining-neighbours-of-cell-as-diamond-shape-in-python
        # figure out if we're in range of y
        if sensor[1] - dist <= y <= sensor[1] + dist:
            # print(sensor, "in range")
            # figure out which "row" we're in
            row = abs(y - sensor[1])
            # print("row", row)
            xdiff = dist - row
            x_min = sensor[0] - xdiff
            x_max = sensor[0] + xdiff
            ranges.append((x_min, x_max))

    sorted_ranges = list(sorted(ranges))

    merged = mergeIntervals([ list(item) for item in sorted_ranges])
    print(merged)
    print(merged[0][1]-merged[0][0])


def part2():
    sensors, beacons = parseInput(15)
    print(sensors)
    num_sensors = len(sensors)
    print(beacons)
    # shortest_dists = []
    y = 4000000
    # y = 20
    y_no_beacons = set()
    ranges = {}
    for i in range(num_sensors):
        dist = manhattan(sensors[i], beacons[i])
        # shortest_dists.append(dist)
        sensor = sensors[i]

        # check "diamond", but only in row y
        # inspired by: https://stackoverflow.com/questions/64823023/determining-neighbours-of-cell-as-diamond-shape-in-python
        # figure out if we're in range of y and x
        for j in range(max(0, sensor[1] - dist), min(y + 1, sensor[1] + dist)):
            # print(j)
            # if sensor[1] - dist <= j <= :
                # print(sensor, "in range")
                # figure out which "row" we're in
            row = abs(sensor[1] - j)

            # print("row", row)
            xdiff = dist - row
            x_min = sensor[0] - xdiff
            x_max = sensor[0] + xdiff
            if ranges.get(j) is None:
                ranges[j] = [[x_min, x_max]]
            else:
                ranges[j] = ranges[j] + [[x_min, x_max]]

    check_ranges = {}
    for j in ranges:
        y_ranges = ranges[j]
        sorted_ranges = list(sorted(y_ranges))

        merged = mergeIntervals([ list(item) for item in sorted_ranges])
        if len(merged) > 1:
            check_ranges[j] = merged
            if len(merged) == 2 and merged[1][0] -1 == merged[0][1]:
                continue
            else:
                print(j, merged)
        # print(merged[0][1]-merged[0][0])

    # TODO: manually did math at the end

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
