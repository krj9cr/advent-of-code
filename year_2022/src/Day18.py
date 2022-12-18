from mpl_toolkits import mplot3d
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

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

def get_surface_area(cubes):
    cube_sides = {}

    max_x = 0
    max_y = 0
    max_z = 0

    for cube in cubes:
        x, y ,z = cube
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        if z > max_z:
            max_z = z
        cube_sides[cube] = 6
        # print("cube", cube)
        for neighbor in get_neighbors(cube):
            # print("neighbor", neighbor)
            if cube_sides.get(neighbor) is not None:
                cube_sides[cube] -= 1
                cube_sides[neighbor] -= 1
        # print("cube_sides", cube_sides)
        # print()
    return sum(cube_sides.values()), max_x, max_y, max_z

def part1():
    cubes = parseInput(18)
    print(cubes)
    print(get_surface_area(cubes))


def find_path_out(empty_cube, input_cubes, holes, not_holes, max_x, max_y, max_z, seen):
    x, y, z = empty_cube
    if x > max_x or y > max_y or z > max_z or x < 0 or y < 0 or z < 0:
        return True
    else:
        seen.add(empty_cube)
        path = False
        for neighbor in get_neighbors(empty_cube):
            if neighbor in input_cubes:
                continue
            # if neighbor in holes:
            #     return False
            # if neighbor in not_holes:
            #     return True
            if neighbor not in seen:
                path = path or find_path_out(neighbor, input_cubes, holes, not_holes, max_x, max_y, max_z, seen)
        return path

def part2():
    cubes = parseInput(18)
    print(cubes)

    total_surface_ara, max_x, max_y, max_z = get_surface_area(cubes)
    print("total_surface_ara", total_surface_ara)
    print("maxes:", max_x, max_y, max_z)

    all_cubes = []
    for k in range(max_z):
        for j in range(max_y):
            for i in range(max_x):
                all_cubes.append((i, j, k))

    empty_cubes = set(all_cubes) - set(cubes)
    print(empty_cubes)

    holes = set()
    not_holes = set()
    hole_groups = []
    # for every empty cube... is there a way outside the perimeter?
    for empty_cube in empty_cubes:
        print("empty_cube", empty_cube)
        is_in_hole = False
        for hole in hole_groups:
            for item in hole:
                if empty_cube == item:
                    is_in_hole = True
                    break
            if is_in_hole:
                break
        if is_in_hole:
            continue
        group = set()
        path = find_path_out(empty_cube, cubes, holes, not_holes, max_x, max_y, max_z, group)
        if not path:
        #     for item in group:
        #         not_holes.add(item)
        # else:
            for item in group:
                holes.add(item)
            hole_groups.append(set(group))

    # make sure there are no duplicate groups?
    # new_groups = []
    # for i in range(len(hole_groups)):
    #     for j in range(len(hole_groups)):
    #         if i == j:
    #             continue
    #         group1 = hole_groups[i]
    #         group2 = hole_groups[j]
    #         if group1 == group2:
    #             print("group", i , "==", j)


    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # c = np.array(holes)
    # ax.scatter3D(c[:, 0], c[:, 1], c[:, 2], c=c[:, 2], cmap='Greens')
    # plt.show()

    print("hole groups", hole_groups)
    sub = 0
    for group in hole_groups:
        sub2, _, _, _ = get_surface_area(group)
        sub += sub2

    print("group area", sub)

    answer = total_surface_ara - sub

    # need to find how many cubes are in each hole... then compute the surface area of the hole and subtract it from total


    print(answer)

if __name__ == "__main__":
    # print("\nPART 1 RESULT")
    # start = time.perf_counter()
    # part1()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)

    import sys

    sys.setrecursionlimit(1500)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
