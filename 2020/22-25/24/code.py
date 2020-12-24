import time
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    l = line.strip()
    dirs = []
    while len(l) >= 1:
        n = l[0]
        if n == "e" or n == "w":
            dirs.append(n)
            l = l[1:]
        else:
            n = l[0:2]
            dirs.append(n)
            l = l[2:]
    return dirs

# https://www.redblobgames.com/grids/hexagons/#coordinates
class Hex:
    def __init__(self, q=0, r=0, color=0):
        self.r = r # row
        self.q = q # column
        self.color = color # 0 for white, 1 for black

    def flipColor(self):
        if self.color == 0:
            self.color = 1
        else:
            self.color = 0

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r

    def __str__(self):
        color = 'white'
        if self.color == 1:
            color = 'black'
        return "(" + str(self.q) + ", " + str(self.r) + ")" + " " + color

ordinal_directions = {
    'w': (-1, 0),
    'nw': (0, -1),
    'sw': (-1, 1),
    'e': (1, 0),
    'ne': (1, -1),
    'se': (0, 1),
}

# lots of good source from:
# https://www.redblobgames.com/grids/hexagons/implementation.html#hex
class HexGrid:
    def __init__(self):
        self.hexes = {(0,0): Hex(0,0)}

    # source: https://stackoverflow.com/questions/59042139/how-to-properly-draw-hexagons-with-offset-coordinates
    def plot(self):
        fig, ax = plt.subplots(1)
        ax.set_aspect('equal')

        for coord in self.hexes:
            h = self.hexes[coord]
            color = (1,1,1)
            if h.color == 1:
                color = (0,0,0)
            q = h.q
            r = h.r
            # if r % 2 == 1:
            #     q -= 0.5
            edgecolor = 'k'
            if q == r == 0:
                edgecolor = (1,0,0)
            hexagon = RegularPolygon((q, r), facecolor=color, numVertices=6, radius=np.sqrt(1/3), alpha=0.5, edgecolor=edgecolor)
            ax.add_patch(hexagon)
        plt.autoscale(enable = True)
        plt.show()

    def count_adj_black(self, h):
        neighbors = self.get_all_existing_neighbors(h)
        count = 0
        for n in neighbors:
            if n.color == 1:
                count += 1
        return count

    def hex_neighbor(self, h, ordinal_direction):
        q, r = ordinal_directions[ordinal_direction]
        # print("adding", h.q, "+", q, "and", h.r, "+",r)
        newq = h.q + q
        newr = h.r + r
        newHex = self.hexes.get((newq, newr))
        if newHex is None:
            newHex = Hex(newq, newr)
            self.hexes[(newq, newr)] = newHex
        return newHex

    def hex_existing_neighbor(self, h, ordinal_direction):
        q, r = ordinal_directions[ordinal_direction]
        newq = h.q + q
        newr = h.r + r
        return self.hexes.get((newq, newr))

    def get_all_existing_neighbors(self, h):
        res = []
        for d in ordinal_directions:
            n = self.hex_existing_neighbor(h, d)
            if n is not None:
                res.append(n)
        return res

    def get_all_possible_neighbors(self, h):
        return [ self.hex_neighbor(h, o) for o in ordinal_directions]

    def count_black(self):
        count = 0
        for coord in self.hexes:
            h = self.hexes[coord]
            if h.color == 1:
                count += 1
        return count

    def grow_from_black(self):
        origKeys = list(self.hexes.keys())[:]
        for coord in origKeys:
            h = self.hexes[coord]
            if h.color == 1:
                self.get_all_possible_neighbors(h)

###########################
# part1
###########################
def part1(data):
    # print(data)
    grid = HexGrid()
    # print([ str(h) for h in grid.hexes])

    for line in data:
        currHex = grid.hexes[(0,0)]
        # print("starting", line, "from",currHex)
        for ordinal_direction in line:
            # print(currHex)
            # axial_direction = ordinal_directions[ordinal_direction]
            nextHex = grid.hex_neighbor(currHex, ordinal_direction)
            currHex = nextHex
        currHex.flipColor()
        # print("ended at", currHex)

    print("num black:",grid.count_black())

    # grid.plot()
    return grid


def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def part2(data):
    grid = part1(data)

    # expand out from black tiles if necessary
    grid.grow_from_black()

    # grid.plot()
    # pass days
    for i in range(1,101):
        newGrid = HexGrid()
        # print(grid.hexes)
        for tileCoord in grid.hexes:
            tile = grid.hexes[tileCoord]
            black_neighbors = grid.count_adj_black(tile)
            if tile.color == 1: # black
                if black_neighbors == 0 or black_neighbors > 2:
                    newGrid.hexes[tileCoord] = Hex(tile.q, tile.r, 0)
                else:
                    newGrid.hexes[tileCoord] = tile
            else: # white
                if black_neighbors == 2:
                    newGrid.hexes[tileCoord] = Hex(tile.q, tile.r, 1)
                else:
                    newGrid.hexes[tileCoord] = tile
        grid = newGrid
        # expand out from black tiles if necessary
        grid.grow_from_black()
        # grid.plot()
        print("Day ", i, ":", grid.count_black())

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
