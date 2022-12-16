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

def part1():
    sensors, beacons = parseInput(15)
    print(sensors)
    num_sensors = len(sensors)
    print(beacons)
    shortest_dists = []
    for i in range(num_sensors):
        dist = manhattan(sensors[i], beacons[i])
        shortest_dists.append(dist)
    # print(shortest_dists)

    y = 2000000
    y_no_beacons = set()

    # generate some diamonds/ranges
    for i in range(num_sensors):
        sensor = sensors[i]
        dist = shortest_dists[i]
        print("Sensor ", i, "out of ", num_sensors)
        # print(sensor, "dist", dist, "checking", sensor[0]+-dist, "to", sensor[0]+dist)

        # check "diamond", but only in row y
        # inspired by: https://stackoverflow.com/questions/64823023/determining-neighbours-of-cell-as-diamond-shape-in-python
        # figure out if we're in range of y
        if sensor[1] - dist <= y <= sensor[1] + dist:
            # print(sensor, "in range")
            # figure out which "row" we're in
            row = abs(y - sensor[1])
            # print("row", row)
            xdiff = dist - abs(row)
            # print("xdiff",xdiff)
            for dx in range(-xdiff, xdiff + 1):
                no_beacon = (sensor[0] + dx, y)
                # print(no_beacon)
                if no_beacon not in beacons:
                    y_no_beacons.add(no_beacon[0])

        print()
    # print(sorted(y_no_beacons))
    print(len(y_no_beacons))


def part2():
    sensors, beacons = parseInput(15)
    print(sensors)
    num_sensors = len(sensors)
    print(beacons)
    shortest_dists = []
    for i in range(num_sensors):
        dist = manhattan(sensors[i], beacons[i])
        shortest_dists.append(dist)
    # print(shortest_dists)

    max_x_y = 20
    y_no_beacons = set()

    # generate some diamonds/ranges
    for i in range(num_sensors):
        sensor = sensors[i]
        dist = shortest_dists[i]
        print("Sensor ", i, "out of ", num_sensors)

        # figure out if we're in range of x and y
        # have a set of all possible coords? ...
        # remove items from the set

        # if sensor[1] - dist <= y <= sensor[1] + dist:
            # print(sensor, "in range")
            # figure out which "row" we're in
            # row = abs(y - sensor[1])
            # print("row", row)
            # xdiff = dist - abs(row)
            # print("xdiff",xdiff)
            # for dx in range(-xdiff, xdiff + 1):
                #no_beacon = (sensor[0] + dx, y)
                # print(no_beacon)
                #if no_beacon not in beacons:
                    #y_no_beacons.add(no_beacon[0])

        print()
    # print(sorted(y_no_beacons))
    print(len(y_no_beacons))

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
