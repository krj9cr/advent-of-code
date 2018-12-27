from functools import reduce


def parseInput(path: str):
    with open(path, 'r') as file:
        return [parseLine(line) for line in file]


def parseLine(line: str):
    return tuple([int(num) for num in line.strip().split(",")])


def dist4D(a, b):
    x1, y1, z1, q1 = a
    x2, y2, z2, q2 = b
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2) + abs(q1 - q2)


def part1(path: str):
    constellations = []
    distance_threshold = 3
    coords = parseInput(path)
    # print(coords)

    # build up a list of each coordinate and its nearby coordinates
    for coord1 in coords:
        nearby_coords = set()
        for coord2 in coords:
            dist = dist4D(coord1, coord2)
            if dist <= distance_threshold:
                nearby_coords.add(coord2)
        constellations.append(nearby_coords)
    # print(constellations)

    # join sets if they have at least one intersection
    while True:
        merged = set()
        for constellation in constellations:
            intersecting_constellations = list(filter(lambda x: len(constellation.intersection(x)) > 0, constellations))
            if len(intersecting_constellations) > 0:
                merged.add(frozenset(reduce(lambda x, y: x.union(y), intersecting_constellations)))
        if constellations == list(merged):
            break
        constellations = list(merged)

    # print(merged)
    print("part1:", len(merged))


def part2(path: str):
    lines = parseInput(path)
    print(lines)
