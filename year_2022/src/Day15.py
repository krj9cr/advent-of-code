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

def get_diamond_neighbors(center, y, n=1):
    ret = []
    for dx in range(-n, n + 1):
        ydiff = n - abs(dx)
        if center[1]+ -ydiff <= y <= center[1] +ydiff + 1:
            ret.append((center[0] + dx, y))
    return ret

def part1():
    sensors, beacons = parseInput(15)
    print(sensors)
    num_sensors = len(sensors)
    print(beacons)
    shortest_dists = []
    for i in range(num_sensors):
        dist = manhattan(sensors[i], beacons[i])
        shortest_dists.append(dist)
    print(shortest_dists)

    y = 2000000
    y_no_beacons = set()

    # generate some diamonds/ranges
    for i in range(num_sensors):
        print("Sensor ", i, "out of ", num_sensors)
        sensor = sensors[i]
        neighbors = get_diamond_neighbors(sensor, y, shortest_dists[i])
        for n in neighbors:
            if n[1] == y and n not in beacons and n not in sensors:
                y_no_beacons.add(n)
    print(sorted(y_no_beacons))
    print(len(y_no_beacons))

# 4502209 too high
# 5543957 too high


def part2():
    lines = parseInput(15)
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
