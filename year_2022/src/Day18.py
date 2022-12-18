import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        # lines = [int(num) for line in file for num in line.strip().split(",")]
        coords = []
        for line in lines:
            coord = []
            for char in line.split(","):
                coord.append(int(char))
            coords.append(tuple(coord))
        return coords

def get_neighbors(coord):
    neighbors = []
    for x, y, z in (0,0,1), (0,0,-1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0):
        neighbors.append(tuple([coord[0]+x, coord[1]+y, coord[2]+z]))
    return neighbors


def part1():
    cubes = parseInput(18)
    print(cubes)
    cube_sides = {}
    for cube in cubes:
        cube_sides[cube] = 6
        print("cube", cube)
        for neighbor in get_neighbors(cube):
            print("neighbor", neighbor)
            if cube_sides.get(neighbor) is not None:
                cube_sides[cube] -= 1
                cube_sides[neighbor] -= 1
        print("cube_sides", cube_sides)
        print()
    print(sum(cube_sides.values()))



def part2():
    lines = parseInput(18)
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
