import time

def part1():
    dayf = "{:02d}".format(2)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        max_red = 12
        max_green = 13
        max_blue = 14
        answer = 0

        for line in file:
            line = line.strip()
            parts = line.split(": ")
            gameId = int(parts[0].strip("Game "))
            all_rounds_possible = True
            for raw_round in parts[1].split(";"):
                for cube in raw_round.split(","):
                    cube_info = cube.strip().split(" ")
                    num_cube = int(cube_info[0])
                    cube_color = cube_info[1]
                    if (cube_color == "red" and num_cube > max_red) or \
                            (cube_color == "green" and num_cube > max_green) or \
                            (cube_color == "blue" and num_cube > max_blue):
                        all_rounds_possible = False
                        break
                if not all_rounds_possible:
                    break
            if all_rounds_possible:
                answer += gameId
        print(answer)

def part2():
    dayf = "{:02d}".format(2)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        answer = 0

        for line in file:
            line = line.strip()
            parts = line.split(": ")
            min_red = 0
            min_green = 0
            min_blue = 0
            for raw_round in parts[1].split(";"):
                for cube in raw_round.split(","):
                    cube_info = cube.strip().split(" ")
                    num_cube = int(cube_info[0])
                    cube_color = cube_info[1]
                    if num_cube > min_red and cube_color == "red":
                        min_red = num_cube
                    if num_cube > min_green and cube_color == "green":
                        min_green = num_cube
                    if num_cube > min_blue and cube_color == "blue":
                        min_blue = num_cube
            answer += (min_red * min_green * min_blue)
        print(answer)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    total = end - start
    print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    total = end - start
    print("Time (ms):", (end - start) * 1000)
