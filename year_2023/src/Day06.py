import time
import re

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        times = [int(t) for t in re.sub(' +', ' ', lines[0].strip("Time:").strip()).split(" ")]
        distances = [int(t) for t in re.sub(' +', ' ', lines[1].strip("Distance:").strip()).split(" ")]
        return times, distances

def part1():
    times, distances = parseInput(6)
    # times = [7]
    print(times)
    print(distances)

    answer = 1
    for i in range(len(times)):
        time = times[i]
        distance = distances[i]

        possible_wins = []
        for t in range(1, time):
            # print(t)
            time_to_travel = time - t
            speed = t
            race_dist = time_to_travel * speed
            if race_dist > distance:
                possible_wins.append(t)
        print("time:", time, "num ways to win:", len(possible_wins))
        answer *= len(possible_wins)
    print(answer)

def part2():
    dayf = "{:02d}".format(6)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        time = int("".join(re.sub(' +', ' ', lines[0].strip("Time:").strip()).split(" ")))
        distance = int("".join(re.sub(' +', ' ', lines[1].strip("Distance:").strip()).split(" ")))

        print(time)
        print(distance)

        possible_wins = []
        for t in range(1, time):
            # print(t)
            time_to_travel = time - t
            speed = t
            race_dist = time_to_travel * speed
            if race_dist > distance:
                possible_wins.append(t)
        print("time:", time, "num ways to win:", len(possible_wins))

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
