import time
import sys
import numpy as np
from copy import deepcopy
import math
import random
from lib.print import print_2d_grid
import part2_helpers

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        # read lines
        rawlines = [line.strip() for line in file]

        # batch them into lists separated by empty line
        batchedlines = []
        currBatch = []
        for line in rawlines:
            if line != '':
                currBatch.append(line)
            else:
                tileNum = int(currBatch[0].replace("Tile ", "").replace(":", ""))
                grid = currBatch[1:]
                grid = [ [ char for char in row] for row in grid ]
                batchedlines.append(tuple([tileNum, np.array(grid)]))
                currBatch = []
        # last one
        tileNum = int(currBatch[0].replace("Tile ", "").replace(":", ""))
        grid = currBatch[1:]
        grid = [ [ char for char in row] for row in grid ]
        batchedlines.append(tuple([tileNum, np.array(grid)]))

        return batchedlines

def parseLine(line: str):
    return line.strip()

def getTileConfigurations(tile):
    res = []
    for i in range(4):
        res.append(np.rot90(tile, k=i))
    t = np.fliplr(tile)
    for i in range(4):
        res.append(np.rot90(t, k=i-4))
    return res

def checkFit(x, y, x2, y2, currentTile, rot):
    # right
    if (x2, y2) == (x + 1, y):
        return (currentTile[:,-1] == rot[:,0]).all()
    # down
    elif (x2,y2) == (x, y + 1):
        return (currentTile[-1,:] == rot[0,:]).all()
    # left
    elif (x2, y2) ==  (x - 1, y):
        return (currentTile[:,0] == rot[:,-1]).all()
    # up
    elif (x2, y2) == (x, y - 1):
        return (currentTile[:,-1] == rot[:,0]).all()
    else:
        print("Whoops")
        sys.exit(1)



###########################
# part1
###########################
def part1(data):
    # print(data)
    # firstNum, firstGrid = data[0]

    tileBorders = {}
    # for each tile, store its 4 borders
    for tileNum, grid in data:
        # top, right, bottom, left
        tileBorders[tileNum] = [grid[0,:], grid[:,-1], grid[-1,:], grid[:,0]]
    print(tileBorders)


    matches = {}
    # init matches
    for tileNum, _ in data:
        matches[tileNum] = {0: set(), 1: set(), 2: set(), 3: set()}

    # find some matches
    for tileNum in tileBorders:
        borders = tileBorders[tileNum]
        for tileNum2 in tileBorders:
            if tileNum2 == tileNum:
                continue
            borders2 = tileBorders[tileNum2]
            for b1 in range(len(borders)):
                for b2 in range(len(borders2)):
                    if (borders[b1] == borders2[b2]).all():
                        # print(tileNum, b1, "matches", tileNum2, b2)
                        matches[tileNum][b1].add(tuple([tileNum2, b2]))
                        # print(borders[b1], borders2[b2])
                        # print()
                    # check flipped matches
                    if (borders[b1] == np.flip(borders2[b2])).all():
                        # print(tileNum, b1, "matches flip", tileNum2, b2+4)
                        matches[tileNum][b1].add(tuple([tileNum2, b2+4]))
                        # print(borders[b1], borders2[b2])
                        # print()

    print(matches)

    # find corners... the 4 tiles with exactly 2 matches for 2 adjacent sides
    corners = []
    edges = []
    middle = []
    unknown = []
    for tileNum in matches:
        sides = matches[tileNum]
        if (len(sides[0]) == len(sides[1]) == 1 and len(sides[2]) == len(sides[3]) == 0) or \
            (len(sides[1]) == len(sides[2]) == 1 and len(sides[3]) == len(sides[0]) == 0) or \
            (len(sides[2]) == len(sides[3]) == 1 and len(sides[0]) == len(sides[1]) == 0) or \
            (len(sides[3]) == len(sides[0]) == 1 and len(sides[1]) == len(sides[2]) == 0):
            corners.append(tileNum)
        elif (len(sides[0]) == len(sides[1]) == len(sides[2]) == 1 and len(sides[3]) == 0) or \
            (len(sides[1]) == len(sides[2]) == len(sides[3]) == 1 and len(sides[0]) == 0) or \
            (len(sides[2]) == len(sides[3]) == len(sides[0]) == 1 and len(sides[1]) == 0) or \
            (len(sides[3]) == len(sides[0]) == len(sides[1]) == 1 and len(sides[2]) == 0):
            edges.append(tileNum)
        elif(len(sides[0]) == len(sides[1]) == len(sides[2]) == len(sides[3]) == 1) or \
            (len(sides[1]) == len(sides[2]) == len(sides[3]) == len(sides[0]) == 1) or \
            (len(sides[2]) == len(sides[3]) == len(sides[0]) == len(sides[1]) == 1) or \
            (len(sides[3]) == len(sides[0]) == len(sides[1]) == len(sides[2]) == 1):
            middle.append(tileNum)
        else:
            unknown.append(tileNum)

    print("Corners",corners)
    print("edges",edges)
    print("middle",middle)
    print("unknown",unknown)
    # add corner id nums
    res = 1
    for corner in corners:
        print(corner, matches[corner])
        res *= corner
    print("PROD", res)

# matches = {2609: {0: {(1237, 0)}, 1: {(2339, 0)}, 2: {(1493, 1)}, 3: {(1913, 7)}}, 3347: {0: {(2467, 2)}, 1: {(2381, 4)}, 2: {(2297, 4)}, 3: set()}, 2801: {0: {(2221, 2)}, 1: {(3797, 5)}, 2: {(2437, 1)}, 3: {(3041, 5)}}, 2851: {0: {(3943, 7)}, 1: {(2503, 7)}, 2: {(1213, 0)}, 3: {(2857, 2)}}, 2297: {0: {(3347, 6)}, 1: set(), 2: {(2053, 7)}, 3: {(3163, 5)}}, 1237: {0: {(2609, 0)}, 1: {(3719, 4)}, 2: {(3931, 2)}, 3: {(2129, 6)}}, 1931: {0: {(3499, 3)}, 1: {(3989, 3)}, 2: {(1993, 6)}, 3: {(2207, 0)}}, 3989: {0: {(3697, 7)}, 1: {(1523, 2)}, 2: {(2789, 3)}, 3: {(1931, 1)}}, 1129: {0: {(1381, 7)}, 1: {(3931, 4)}, 2: {(2593, 3)}, 3: set()}, 3491: {0: {(1061, 6)}, 1: {(2011, 0)}, 2: {(3691, 4)}, 3: {(2083, 6)}}, 1607: {0: {(3673, 6)}, 1: set(), 2: {(3967, 2)}, 3: {(3301, 2)}}, 3307: {0: {(1613, 5)}, 1: {(1321, 1)}, 2: set(), 3: {(1187, 6)}}, 3931: {0: {(1129, 5)}, 1: {(1597, 5)}, 2: {(1237, 2)}, 3: {(1979, 0)}}, 2011: {0: {(3491, 1)}, 1: {(2161, 3)}, 2: {(3529, 3)}, 3: {(2339, 6)}}, 1033: {0: {(3637, 0)}, 1: {(1277, 3)}, 2: {(2081, 2)}, 3: {(3821, 0)}}, 3761: {0: {(2729, 2)}, 1: {(2207, 2)}, 2: {(3671, 2)}, 3: {(2819, 5)}}, 1277: {0: {(1543, 7)}, 1: {(3019, 0)}, 2: {(2729, 0)}, 3: {(1033, 1)}}, 1487: {0: {(2879, 0)}, 1: {(2417, 2)}, 2: {(2861, 4)}, 3: {(1217, 1)}}, 3617: {0: {(2389, 4)}, 1: {(2963, 1)}, 2: {(3821, 6)}, 3: {(1877, 3)}}, 3121: {0: set(), 1: set(), 2: {(2053, 5)}, 3: {(1583, 7)}}, 2017: {0: {(2311, 6)}, 1: {(1787, 5)}, 2: {(1427, 1)}, 3: {(3259, 2)}}, 3119: {0: {(1747, 7)}, 1: {(2287, 5)}, 2: {(2113, 6)}, 3: {(3623, 5)}}, 1933: {0: {(1103, 4)}, 1: {(1327, 7)}, 2: {(3299, 3)}, 3: {(1181, 2)}}, 1597: {0: {(3719, 7)}, 1: {(3931, 5)}, 2: {(1381, 4)}, 3: {(1097, 6)}}, 2467: {0: {(3877, 2)}, 1: {(2243, 7)}, 2: {(3347, 0)}, 3: set()}, 1427: {0: {(1481, 0)}, 1: {(2017, 2)}, 2: {(1861, 1)}, 3: set()}, 2351: {0: {(2311, 3)}, 1: {(1787, 6)}, 2: {(2647, 0)}, 3: {(2557, 7)}}, 2243: {0: {(2381, 1)}, 1: {(1877, 1)}, 2: {(2833, 6)}, 3: {(2467, 5)}}, 3163: {0: {(3041, 4)}, 1: {(2297, 7)}, 2: {(2381, 7)}, 3: {(2437, 4)}}, 2281: {0: {(1013, 7)}, 1: {(2099, 6)}, 2: {(1571, 5)}, 3: {(1451, 4)}}, 2213: {0: {(3671, 1)}, 1: {(2207, 5)}, 2: {(1993, 1)}, 3: set()}, 1097: {0: {(3259, 4)}, 1: {(3529, 5)}, 2: {(1597, 7)}, 3: {(2549, 2)}}, 3821: {0: {(1033, 3)}, 1: {(1039, 2)}, 2: {(3617, 6)}, 3: {(3181, 0)}}, 2699: {0: {(1747, 0)}, 1: set(), 2: {(3253, 1)}, 3: {(2287, 6)}}, 1231: {0: {(1013, 1)}, 1: {(2113, 4)}, 2: {(3943, 0)}, 3: {(2503, 6)}}, 3631: {0: {(1213, 7)}, 1: {(2857, 5)}, 2: {(2357, 5)}, 3: {(2069, 5)}}, 1913: {0: {(2963, 0)}, 1: {(2389, 3)}, 2: {(2129, 5)}, 3: {(2609, 7)}}, 1013: {0: {(3299, 1)}, 1: {(1231, 0)}, 2: {(2711, 2)}, 3: {(2281, 4)}}, 1181: {0: {(3803, 7)}, 1: {(2099, 0)}, 2: {(1933, 3)}, 3: {(3659, 6)}}, 2671: {0: {(1579, 2)}, 1: {(1901, 6)}, 2: {(1283, 4)}, 3: {(2137, 6)}}, 1721: {0: {(2437, 2)}, 1: {(3797, 4)}, 2: {(2129, 4)}, 3: {(2389, 6)}}, 1877: {0: {(1091, 6)}, 1: {(2243, 1)}, 2: {(1039, 5)}, 3: {(3617, 3)}}, 1889: {0: set(), 1: {(1861, 3)}, 2: {(3361, 3)}, 3: set()}, 1091: {0: {(2437, 3)}, 1: {(2389, 5)}, 2: {(1877, 4)}, 3: {(2381, 2)}}, 2161: {0: {(3691, 3)}, 1: {(3511, 7)}, 2: {(3727, 0)}, 3: {(2011, 1)}}, 3253: {0: {(2777, 5)}, 1: {(2699, 2)}, 2: set(), 3: {(1201, 6)}}, 3079: {0: {(1283, 7)}, 1: {(1901, 7)}, 2: {(2777, 3)}, 3: {(3643, 5)}}, 1201: {0: {(2861, 5)}, 1: {(1217, 6)}, 2: {(3253, 7)}, 3: set()}, 3797: {0: {(1721, 5)}, 1: {(2801, 5)}, 2: {(3331, 6)}, 3: {(1979, 6)}}, 2311: {0: {(3511, 4)}, 1: {(3727, 1)}, 2: {(2017, 4)}, 3: {(2351, 0)}}, 1187: {0: set(), 1: {(1453, 5)}, 2: {(3307, 7)}, 3: set()}, 3259: {0: {(1097, 4)}, 1: {(1481, 5)}, 2: {(2017, 3)}, 3: {(3727, 2)}}, 3019: {0: {(1277, 1)}, 1: {(3929, 6)}, 2: {(2677, 6)}, 3: {(1579, 0)}}, 1979: {0: {(3931, 3)}, 1: {(2129, 7)}, 2: {(3797, 7)}, 3: {(2593, 2)}}, 2287: {0: {(3643, 4)}, 1: {(3119, 5)}, 2: {(2699, 7)}, 3: {(2777, 0)}}, 2437: {0: {(3163, 7)}, 1: {(2801, 2)}, 2: {(1721, 0)}, 3: {(1091, 0)}}, 1571: {0: {(1009, 2)}, 1: {(2281, 6)}, 2: {(1321, 7)}, 3: set()}, 2833: {0: {(2819, 7)}, 1: {(3877, 1)}, 2: {(2243, 6)}, 3: {(1039, 0)}}, 2861: {0: {(1487, 6)}, 1: {(1201, 4)}, 2: set(), 3: {(1051, 5)}}, 3361: {0: set(), 1: {(2647, 5)}, 2: {(1787, 3)}, 3: {(1889, 2)}}, 3929: {0: {(2207, 3)}, 1: {(2729, 5)}, 2: {(3019, 5)}, 3: {(3499, 0)}}, 2711: {0: {(3623, 0)}, 1: {(2113, 5)}, 2: {(1013, 2)}, 3: {(1451, 5)}}, 2789: {0: {(1993, 7)}, 1: set(), 2: {(1789, 6)}, 3: {(3989, 2)}}, 3511: {0: {(2311, 4)}, 1: {(2557, 2)}, 2: {(2683, 3)}, 3: {(2161, 5)}}, 2417: {0: {(3697, 5)}, 1: {(1051, 2)}, 2: {(1487, 1)}, 3: {(2677, 0)}}, 1453: {0: {(1613, 2)}, 1: {(1187, 5)}, 2: set(), 3: {(1847, 7)}}, 3727: {0: {(2161, 2)}, 1: {(2311, 1)}, 2: {(3259, 3)}, 3: {(3529, 2)}}, 1061: {0: {(1493, 6)}, 1: {(2069, 3)}, 2: {(3491, 4)}, 3: {(2339, 1)}}, 2389: {0: {(3617, 4)}, 1: {(1091, 5)}, 2: {(1721, 7)}, 3: {(1913, 1)}}, 2113: {0: {(1231, 5)}, 1: {(2711, 5)}, 2: {(3119, 6)}, 3: {(3643, 7)}}, 1741: {0: set(), 1: {(1051, 3)}, 2: {(3697, 0)}, 3: {(1523, 3)}}, 1283: {0: {(2671, 6)}, 1: {(2857, 3)}, 2: {(3943, 6)}, 3: {(3079, 4)}}, 1901: {0: {(1217, 0)}, 1: {(2879, 3)}, 2: {(2671, 5)}, 3: {(3079, 5)}}, 2357: {0: {(2137, 4)}, 1: {(3631, 6)}, 2: {(2803, 4)}, 3: {(3637, 6)}}, 3529: {0: {(3719, 6)}, 1: {(1097, 5)}, 2: {(3727, 3)}, 3: {(2011, 2)}}, 1039: {0: {(2833, 3)}, 1: {(1877, 6)}, 2: {(3821, 1)}, 3: {(2081, 3)}}, 2963: {0: {(1913, 0)}, 1: {(3617, 1)}, 2: {(3181, 5)}, 3: {(1493, 4)}}, 2557: {0: {(3967, 3)}, 1: {(3301, 5)}, 2: {(3511, 1)}, 3: {(2351, 7)}}, 1523: {0: set(), 1: {(1789, 1)}, 2: {(3989, 1)}, 3: {(1741, 3)}}, 1789: {0: set(), 1: {(1523, 1)}, 2: {(2789, 6)}, 3: set()}, 3049: {0: {(2083, 3)}, 1: {(3691, 1)}, 2: {(1103, 3)}, 3: {(1327, 6)}}, 3719: {0: {(1237, 5)}, 1: {(2339, 3)}, 2: {(3529, 4)}, 3: {(1597, 4)}}, 2069: {0: {(2803, 7)}, 1: {(3631, 7)}, 2: {(2083, 5)}, 3: {(1061, 1)}}, 2083: {0: {(1213, 6)}, 1: {(2069, 6)}, 2: {(3491, 7)}, 3: {(3049, 0)}}, 3671: {0: set(), 1: {(2213, 0)}, 2: {(3761, 2)}, 3: {(3319, 2)}}, 1103: {0: {(1933, 4)}, 1: {(3659, 7)}, 2: {(2683, 1)}, 3: {(3049, 2)}}, 3643: {0: {(2287, 4)}, 1: {(3079, 7)}, 2: {(3943, 1)}, 3: {(2113, 7)}}, 3499: {0: {(3929, 3)}, 1: {(2677, 7)}, 2: {(3697, 2)}, 3: {(1931, 0)}}, 2503: {0: {(1327, 4)}, 1: {(3299, 2)}, 2: {(1231, 7)}, 3: {(2851, 5)}}, 2729: {0: {(1277, 2)}, 1: {(3929, 5)}, 2: {(3761, 0)}, 3: {(2081, 5)}}, 2221: {0: set(), 1: {(3331, 3)}, 2: {(2801, 0)}, 3: {(1583, 5)}}, 2129: {0: {(1721, 6)}, 1: {(1913, 6)}, 2: {(1237, 7)}, 3: {(1979, 5)}}, 1217: {0: {(1901, 0)}, 1: {(1487, 3)}, 2: {(1201, 5)}, 3: {(2777, 2)}}, 3967: {0: {(2647, 3)}, 1: set(), 2: {(1607, 2)}, 3: {(2557, 0)}}, 2339: {0: {(2609, 1)}, 1: {(1061, 3)}, 2: {(2011, 7)}, 3: {(3719, 1)}}, 1579: {0: {(3019, 3)}, 1: {(2879, 6)}, 2: {(2671, 0)}, 3: {(1543, 0)}}, 2683: {0: {(3691, 2)}, 1: {(1103, 2)}, 2: {(3301, 4)}, 3: {(3511, 2)}}, 1993: {0: set(), 1: {(2213, 2)}, 2: {(1931, 6)}, 3: {(2789, 4)}}, 2777: {0: {(2287, 3)}, 1: {(3253, 4)}, 2: {(1217, 3)}, 3: {(3079, 2)}}, 2081: {0: {(2819, 2)}, 1: {(2729, 7)}, 2: {(1033, 2)}, 3: {(1039, 3)}}, 1009: {0: {(3803, 4)}, 1: {(2099, 3)}, 2: {(1571, 0)}, 3: set()}, 1543: {0: {(1579, 3)}, 1: {(2137, 5)}, 2: {(3637, 1)}, 3: {(1277, 4)}}, 3877: {0: {(3319, 0)}, 1: {(2833, 1)}, 2: {(2467, 0)}, 3: set()}, 2857: {0: {(2137, 7)}, 1: {(3631, 5)}, 2: {(2851, 3)}, 3: {(1283, 1)}}, 1481: {0: {(1427, 0)}, 1: {(3259, 5)}, 2: {(2549, 3)}, 3: set()}, 1583: {0: {(3041, 2)}, 1: {(2221, 7)}, 2: set(), 3: {(3121, 7)}}, 1861: {0: set(), 1: {(1427, 2)}, 2: {(1787, 0)}, 3: {(1889, 1)}}, 2099: {0: {(1181, 1)}, 1: {(3299, 0)}, 2: {(2281, 5)}, 3: {(1009, 1)}}, 2819: {0: {(3319, 1)}, 1: {(3761, 7)}, 2: {(2081, 0)}, 3: {(2833, 4)}}, 3803: {0: {(1009, 4)}, 1: set(), 2: {(3673, 4)}, 3: {(1181, 4)}}, 2803: {0: {(2357, 6)}, 1: {(3181, 2)}, 2: {(1493, 7)}, 3: {(2069, 4)}}, 1747: {0: {(2699, 0)}, 1: set(), 2: {(1847, 5)}, 3: {(3119, 4)}}, 2137: {0: {(2357, 4)}, 1: {(1543, 5)}, 2: {(2671, 7)}, 3: {(2857, 4)}}, 1847: {0: set(), 1: {(1747, 6)}, 2: {(3623, 2)}, 3: {(1453, 7)}}, 2381: {0: {(3347, 5)}, 1: {(2243, 0)}, 2: {(1091, 3)}, 3: {(3163, 6)}}, 3659: {0: {(3301, 3)}, 1: {(3673, 5)}, 2: {(1181, 7)}, 3: {(1103, 5)}}, 2207: {0: {(1931, 3)}, 1: {(2213, 5)}, 2: {(3761, 1)}, 3: {(3929, 0)}}, 2879: {0: {(1487, 0)}, 1: {(2677, 1)}, 2: {(1579, 5)}, 3: {(1901, 1)}}, 1321: {0: {(1451, 3)}, 1: {(3307, 1)}, 2: set(), 3: {(1571, 6)}}, 3331: {0: set(), 1: {(2593, 1)}, 2: {(3797, 6)}, 3: {(2221, 1)}}, 3623: {0: {(2711, 0)}, 1: {(3119, 7)}, 2: {(1847, 2)}, 3: {(1613, 3)}}, 3637: {0: {(1033, 0)}, 1: {(1543, 2)}, 2: {(2357, 7)}, 3: {(3181, 3)}}, 2677: {0: {(2417, 3)}, 1: {(2879, 1)}, 2: {(3019, 6)}, 3: {(3499, 5)}}, 3299: {0: {(2099, 1)}, 1: {(1013, 0)}, 2: {(2503, 1)}, 3: {(1933, 2)}}, 2647: {0: {(2351, 2)}, 1: {(3361, 5)}, 2: set(), 3: {(3967, 0)}}, 3943: {0: {(1231, 2)}, 1: {(3643, 2)}, 2: {(1283, 6)}, 3: {(2851, 4)}}, 2593: {0: set(), 1: {(3331, 1)}, 2: {(1979, 3)}, 3: {(1129, 2)}}, 3181: {0: {(3821, 3)}, 1: {(2963, 6)}, 2: {(2803, 1)}, 3: {(3637, 3)}}, 3697: {0: {(1741, 2)}, 1: {(2417, 4)}, 2: {(3499, 2)}, 3: {(3989, 4)}}, 1213: {0: {(2851, 2)}, 1: {(1327, 1)}, 2: {(2083, 4)}, 3: {(3631, 4)}}, 2053: {0: set(), 1: {(3121, 6)}, 2: {(3041, 3)}, 3: {(2297, 6)}}, 2549: {0: set(), 1: {(1381, 5)}, 2: {(1097, 3)}, 3: {(1481, 2)}}, 1451: {0: {(2281, 7)}, 1: {(2711, 7)}, 2: {(1613, 4)}, 3: {(1321, 0)}}, 1613: {0: {(1451, 6)}, 1: {(3307, 4)}, 2: {(1453, 0)}, 3: {(3623, 3)}}, 3301: {0: {(2683, 6)}, 1: {(2557, 5)}, 2: {(1607, 3)}, 3: {(3659, 0)}}, 1787: {0: {(1861, 2)}, 1: {(2017, 5)}, 2: {(2351, 5)}, 3: {(3361, 2)}}, 1051: {0: set(), 1: {(2861, 7)}, 2: {(2417, 1)}, 3: {(1741, 1)}}, 3041: {0: {(3163, 4)}, 1: {(2801, 7)}, 2: {(1583, 0)}, 3: {(2053, 2)}}, 3691: {0: {(3491, 6)}, 1: {(3049, 1)}, 2: {(2683, 0)}, 3: {(2161, 0)}}, 3319: {0: {(3877, 0)}, 1: {(2819, 0)}, 2: {(3671, 3)}, 3: set()}, 1381: {0: {(1597, 6)}, 1: {(2549, 5)}, 2: set(), 3: {(1129, 4)}}, 3673: {0: {(3803, 6)}, 1: {(3659, 5)}, 2: {(1607, 4)}, 3: set()}, 1493: {0: {(2963, 7)}, 1: {(2609, 2)}, 2: {(1061, 4)}, 3: {(2803, 6)}}, 1327: {0: {(2503, 4)}, 1: {(1213, 1)}, 2: {(3049, 7)}, 3: {(1933, 5)}}}
# corners = [3121, 1889, 1187, 1789]
# edges = [3347, 2297, 1129, 1607, 3307, 2467, 1427, 2213, 2699, 3253, 1201, 1571, 2861, 3361, 2789, 1453, 1741, 1523, 3671, 2221, 3967, 1993, 1009, 3877, 1481, 1583, 1861, 3803, 1747, 1847, 1321, 3331, 2647, 2593, 2053, 2549, 1051, 3319, 1381, 3673]
# middle = [2609, 2801, 2851, 1237, 1931, 3989, 3491, 3931, 2011, 1033, 3761, 1277, 1487, 3617, 2017, 3119, 1933, 1597, 2351, 2243, 3163, 2281, 1097, 3821, 1231, 3631, 1913, 1013, 1181, 2671, 1721, 1877, 1091, 2161, 3079, 3797, 2311, 3259, 3019, 1979, 2287, 2437, 2833, 3929, 2711, 3511, 2417, 3727, 1061, 2389, 2113, 1283, 1901, 2357, 3529, 1039, 2963, 2557, 3049, 3719, 2069, 2083, 1103, 3643, 3499, 2503, 2729, 2129, 1217, 2339, 1579, 2683, 2777, 2081, 1543, 2857, 2099, 2819, 2803, 2137, 2381, 3659, 2207, 2879, 3623, 3637, 2677, 3299, 3943, 3181, 3697, 1213, 1451, 1613, 3301, 1787, 3041, 3691, 1493, 1327]

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def checkGrid(tileNums2d, tiles):
    # print("RRR",tileNums2d)
    # print(tiles)
    w = len(tileNums2d[0])
    h = len(tileNums2d)
    for j in range(h):
        row = tileNums2d[j]
        for i in range(w):
            tileNum = row[i]
            grid = tiles[tileNum]
            # check top
            if j - 1 >= 0:
                grid2 = tiles[tileNums2d[j-1][i]]
                if not (grid[0,:] == grid2[-1,:]).all():
                    return False
            # check bottom
            if j + 1 < h:
                grid2 = tiles[tileNums2d[j+1][i]]
                if not (grid[-1,:] == grid2[0,:]).all():
                    return False
            # check left
            if i - 1 >= 0:
                grid2 = tiles[tileNums2d[j][i-1]]
                if not (grid[:,0] == grid2[:,-1]).all():
                    return False
            # check right
            if i+ 1 < w:
                grid2 = tiles[tileNums2d[j][i+1]]
                if not (grid[:,-1] == grid2[:,0]).all():
                    return False
    return True

def getRandomTiles(data):
    newTiles = {}
    for tileNum, tile in data:
        orientation = random.randint(0, 7)
        if orientation == 0:
            newTiles[tileNum] = tile
        elif orientation < 4:
            newTiles[tileNum] = np.rot90(tile, k=orientation-1)
        else:
            t = np.fliplr(tile)
            if orientation == 4:
                newTiles[tileNum] = t
            else:
                newTiles[tileNum] = np.rot90(t, k=orientation-4)
    return newTiles

def getTileNumMatchingTileNums(tileNum, matches):
    d = matches[tileNum]
    res = []
    for s in d.values():
        if len(s) > 0:
            res.append(s.pop()[0])
    return res

def part2(data):
    # print(data)

    tiles = {}
    for tileNum, tile in data:
        tiles[tileNum] = tile

    dim = int(math.sqrt(len(data)))
    # a grid of grids
    biggoGriddo = []
    tileGrid = []
    for j in range(dim):
        row = []
        for i in range(dim):
            row.append(None)
        biggoGriddo.append(row)
        tileGrid.append(deepcopy(row))

    # real matches
    # matches = {2609: {0: {(1237, 0)}, 1: {(2339, 0)}, 2: {(1493, 1)}, 3: {(1913, 7)}}, 3347: {0: {(2467, 2)}, 1: {(2381, 4)}, 2: {(2297, 4)}, 3: set()}, 2801: {0: {(2221, 2)}, 1: {(3797, 5)}, 2: {(2437, 1)}, 3: {(3041, 5)}}, 2851: {0: {(3943, 7)}, 1: {(2503, 7)}, 2: {(1213, 0)}, 3: {(2857, 2)}}, 2297: {0: {(3347, 6)}, 1: set(), 2: {(2053, 7)}, 3: {(3163, 5)}}, 1237: {0: {(2609, 0)}, 1: {(3719, 4)}, 2: {(3931, 2)}, 3: {(2129, 6)}}, 1931: {0: {(3499, 3)}, 1: {(3989, 3)}, 2: {(1993, 6)}, 3: {(2207, 0)}}, 3989: {0: {(3697, 7)}, 1: {(1523, 2)}, 2: {(2789, 3)}, 3: {(1931, 1)}}, 1129: {0: {(1381, 7)}, 1: {(3931, 4)}, 2: {(2593, 3)}, 3: set()}, 3491: {0: {(1061, 6)}, 1: {(2011, 0)}, 2: {(3691, 4)}, 3: {(2083, 6)}}, 1607: {0: {(3673, 6)}, 1: set(), 2: {(3967, 2)}, 3: {(3301, 2)}}, 3307: {0: {(1613, 5)}, 1: {(1321, 1)}, 2: set(), 3: {(1187, 6)}}, 3931: {0: {(1129, 5)}, 1: {(1597, 5)}, 2: {(1237, 2)}, 3: {(1979, 0)}}, 2011: {0: {(3491, 1)}, 1: {(2161, 3)}, 2: {(3529, 3)}, 3: {(2339, 6)}}, 1033: {0: {(3637, 0)}, 1: {(1277, 3)}, 2: {(2081, 2)}, 3: {(3821, 0)}}, 3761: {0: {(2729, 2)}, 1: {(2207, 2)}, 2: {(3671, 2)}, 3: {(2819, 5)}}, 1277: {0: {(1543, 7)}, 1: {(3019, 0)}, 2: {(2729, 0)}, 3: {(1033, 1)}}, 1487: {0: {(2879, 0)}, 1: {(2417, 2)}, 2: {(2861, 4)}, 3: {(1217, 1)}}, 3617: {0: {(2389, 4)}, 1: {(2963, 1)}, 2: {(3821, 6)}, 3: {(1877, 3)}}, 3121: {0: set(), 1: set(), 2: {(2053, 5)}, 3: {(1583, 7)}}, 2017: {0: {(2311, 6)}, 1: {(1787, 5)}, 2: {(1427, 1)}, 3: {(3259, 2)}}, 3119: {0: {(1747, 7)}, 1: {(2287, 5)}, 2: {(2113, 6)}, 3: {(3623, 5)}}, 1933: {0: {(1103, 4)}, 1: {(1327, 7)}, 2: {(3299, 3)}, 3: {(1181, 2)}}, 1597: {0: {(3719, 7)}, 1: {(3931, 5)}, 2: {(1381, 4)}, 3: {(1097, 6)}}, 2467: {0: {(3877, 2)}, 1: {(2243, 7)}, 2: {(3347, 0)}, 3: set()}, 1427: {0: {(1481, 0)}, 1: {(2017, 2)}, 2: {(1861, 1)}, 3: set()}, 2351: {0: {(2311, 3)}, 1: {(1787, 6)}, 2: {(2647, 0)}, 3: {(2557, 7)}}, 2243: {0: {(2381, 1)}, 1: {(1877, 1)}, 2: {(2833, 6)}, 3: {(2467, 5)}}, 3163: {0: {(3041, 4)}, 1: {(2297, 7)}, 2: {(2381, 7)}, 3: {(2437, 4)}}, 2281: {0: {(1013, 7)}, 1: {(2099, 6)}, 2: {(1571, 5)}, 3: {(1451, 4)}}, 2213: {0: {(3671, 1)}, 1: {(2207, 5)}, 2: {(1993, 1)}, 3: set()}, 1097: {0: {(3259, 4)}, 1: {(3529, 5)}, 2: {(1597, 7)}, 3: {(2549, 2)}}, 3821: {0: {(1033, 3)}, 1: {(1039, 2)}, 2: {(3617, 6)}, 3: {(3181, 0)}}, 2699: {0: {(1747, 0)}, 1: set(), 2: {(3253, 1)}, 3: {(2287, 6)}}, 1231: {0: {(1013, 1)}, 1: {(2113, 4)}, 2: {(3943, 0)}, 3: {(2503, 6)}}, 3631: {0: {(1213, 7)}, 1: {(2857, 5)}, 2: {(2357, 5)}, 3: {(2069, 5)}}, 1913: {0: {(2963, 0)}, 1: {(2389, 3)}, 2: {(2129, 5)}, 3: {(2609, 7)}}, 1013: {0: {(3299, 1)}, 1: {(1231, 0)}, 2: {(2711, 2)}, 3: {(2281, 4)}}, 1181: {0: {(3803, 7)}, 1: {(2099, 0)}, 2: {(1933, 3)}, 3: {(3659, 6)}}, 2671: {0: {(1579, 2)}, 1: {(1901, 6)}, 2: {(1283, 4)}, 3: {(2137, 6)}}, 1721: {0: {(2437, 2)}, 1: {(3797, 4)}, 2: {(2129, 4)}, 3: {(2389, 6)}}, 1877: {0: {(1091, 6)}, 1: {(2243, 1)}, 2: {(1039, 5)}, 3: {(3617, 3)}}, 1889: {0: set(), 1: {(1861, 3)}, 2: {(3361, 3)}, 3: set()}, 1091: {0: {(2437, 3)}, 1: {(2389, 5)}, 2: {(1877, 4)}, 3: {(2381, 2)}}, 2161: {0: {(3691, 3)}, 1: {(3511, 7)}, 2: {(3727, 0)}, 3: {(2011, 1)}}, 3253: {0: {(2777, 5)}, 1: {(2699, 2)}, 2: set(), 3: {(1201, 6)}}, 3079: {0: {(1283, 7)}, 1: {(1901, 7)}, 2: {(2777, 3)}, 3: {(3643, 5)}}, 1201: {0: {(2861, 5)}, 1: {(1217, 6)}, 2: {(3253, 7)}, 3: set()}, 3797: {0: {(1721, 5)}, 1: {(2801, 5)}, 2: {(3331, 6)}, 3: {(1979, 6)}}, 2311: {0: {(3511, 4)}, 1: {(3727, 1)}, 2: {(2017, 4)}, 3: {(2351, 0)}}, 1187: {0: set(), 1: {(1453, 5)}, 2: {(3307, 7)}, 3: set()}, 3259: {0: {(1097, 4)}, 1: {(1481, 5)}, 2: {(2017, 3)}, 3: {(3727, 2)}}, 3019: {0: {(1277, 1)}, 1: {(3929, 6)}, 2: {(2677, 6)}, 3: {(1579, 0)}}, 1979: {0: {(3931, 3)}, 1: {(2129, 7)}, 2: {(3797, 7)}, 3: {(2593, 2)}}, 2287: {0: {(3643, 4)}, 1: {(3119, 5)}, 2: {(2699, 7)}, 3: {(2777, 0)}}, 2437: {0: {(3163, 7)}, 1: {(2801, 2)}, 2: {(1721, 0)}, 3: {(1091, 0)}}, 1571: {0: {(1009, 2)}, 1: {(2281, 6)}, 2: {(1321, 7)}, 3: set()}, 2833: {0: {(2819, 7)}, 1: {(3877, 1)}, 2: {(2243, 6)}, 3: {(1039, 0)}}, 2861: {0: {(1487, 6)}, 1: {(1201, 4)}, 2: set(), 3: {(1051, 5)}}, 3361: {0: set(), 1: {(2647, 5)}, 2: {(1787, 3)}, 3: {(1889, 2)}}, 3929: {0: {(2207, 3)}, 1: {(2729, 5)}, 2: {(3019, 5)}, 3: {(3499, 0)}}, 2711: {0: {(3623, 0)}, 1: {(2113, 5)}, 2: {(1013, 2)}, 3: {(1451, 5)}}, 2789: {0: {(1993, 7)}, 1: set(), 2: {(1789, 6)}, 3: {(3989, 2)}}, 3511: {0: {(2311, 4)}, 1: {(2557, 2)}, 2: {(2683, 3)}, 3: {(2161, 5)}}, 2417: {0: {(3697, 5)}, 1: {(1051, 2)}, 2: {(1487, 1)}, 3: {(2677, 0)}}, 1453: {0: {(1613, 2)}, 1: {(1187, 5)}, 2: set(), 3: {(1847, 7)}}, 3727: {0: {(2161, 2)}, 1: {(2311, 1)}, 2: {(3259, 3)}, 3: {(3529, 2)}}, 1061: {0: {(1493, 6)}, 1: {(2069, 3)}, 2: {(3491, 4)}, 3: {(2339, 1)}}, 2389: {0: {(3617, 4)}, 1: {(1091, 5)}, 2: {(1721, 7)}, 3: {(1913, 1)}}, 2113: {0: {(1231, 5)}, 1: {(2711, 5)}, 2: {(3119, 6)}, 3: {(3643, 7)}}, 1741: {0: set(), 1: {(1051, 3)}, 2: {(3697, 0)}, 3: {(1523, 3)}}, 1283: {0: {(2671, 6)}, 1: {(2857, 3)}, 2: {(3943, 6)}, 3: {(3079, 4)}}, 1901: {0: {(1217, 0)}, 1: {(2879, 3)}, 2: {(2671, 5)}, 3: {(3079, 5)}}, 2357: {0: {(2137, 4)}, 1: {(3631, 6)}, 2: {(2803, 4)}, 3: {(3637, 6)}}, 3529: {0: {(3719, 6)}, 1: {(1097, 5)}, 2: {(3727, 3)}, 3: {(2011, 2)}}, 1039: {0: {(2833, 3)}, 1: {(1877, 6)}, 2: {(3821, 1)}, 3: {(2081, 3)}}, 2963: {0: {(1913, 0)}, 1: {(3617, 1)}, 2: {(3181, 5)}, 3: {(1493, 4)}}, 2557: {0: {(3967, 3)}, 1: {(3301, 5)}, 2: {(3511, 1)}, 3: {(2351, 7)}}, 1523: {0: set(), 1: {(1789, 1)}, 2: {(3989, 1)}, 3: {(1741, 3)}}, 1789: {0: set(), 1: {(1523, 1)}, 2: {(2789, 6)}, 3: set()}, 3049: {0: {(2083, 3)}, 1: {(3691, 1)}, 2: {(1103, 3)}, 3: {(1327, 6)}}, 3719: {0: {(1237, 5)}, 1: {(2339, 3)}, 2: {(3529, 4)}, 3: {(1597, 4)}}, 2069: {0: {(2803, 7)}, 1: {(3631, 7)}, 2: {(2083, 5)}, 3: {(1061, 1)}}, 2083: {0: {(1213, 6)}, 1: {(2069, 6)}, 2: {(3491, 7)}, 3: {(3049, 0)}}, 3671: {0: set(), 1: {(2213, 0)}, 2: {(3761, 2)}, 3: {(3319, 2)}}, 1103: {0: {(1933, 4)}, 1: {(3659, 7)}, 2: {(2683, 1)}, 3: {(3049, 2)}}, 3643: {0: {(2287, 4)}, 1: {(3079, 7)}, 2: {(3943, 1)}, 3: {(2113, 7)}}, 3499: {0: {(3929, 3)}, 1: {(2677, 7)}, 2: {(3697, 2)}, 3: {(1931, 0)}}, 2503: {0: {(1327, 4)}, 1: {(3299, 2)}, 2: {(1231, 7)}, 3: {(2851, 5)}}, 2729: {0: {(1277, 2)}, 1: {(3929, 5)}, 2: {(3761, 0)}, 3: {(2081, 5)}}, 2221: {0: set(), 1: {(3331, 3)}, 2: {(2801, 0)}, 3: {(1583, 5)}}, 2129: {0: {(1721, 6)}, 1: {(1913, 6)}, 2: {(1237, 7)}, 3: {(1979, 5)}}, 1217: {0: {(1901, 0)}, 1: {(1487, 3)}, 2: {(1201, 5)}, 3: {(2777, 2)}}, 3967: {0: {(2647, 3)}, 1: set(), 2: {(1607, 2)}, 3: {(2557, 0)}}, 2339: {0: {(2609, 1)}, 1: {(1061, 3)}, 2: {(2011, 7)}, 3: {(3719, 1)}}, 1579: {0: {(3019, 3)}, 1: {(2879, 6)}, 2: {(2671, 0)}, 3: {(1543, 0)}}, 2683: {0: {(3691, 2)}, 1: {(1103, 2)}, 2: {(3301, 4)}, 3: {(3511, 2)}}, 1993: {0: set(), 1: {(2213, 2)}, 2: {(1931, 6)}, 3: {(2789, 4)}}, 2777: {0: {(2287, 3)}, 1: {(3253, 4)}, 2: {(1217, 3)}, 3: {(3079, 2)}}, 2081: {0: {(2819, 2)}, 1: {(2729, 7)}, 2: {(1033, 2)}, 3: {(1039, 3)}}, 1009: {0: {(3803, 4)}, 1: {(2099, 3)}, 2: {(1571, 0)}, 3: set()}, 1543: {0: {(1579, 3)}, 1: {(2137, 5)}, 2: {(3637, 1)}, 3: {(1277, 4)}}, 3877: {0: {(3319, 0)}, 1: {(2833, 1)}, 2: {(2467, 0)}, 3: set()}, 2857: {0: {(2137, 7)}, 1: {(3631, 5)}, 2: {(2851, 3)}, 3: {(1283, 1)}}, 1481: {0: {(1427, 0)}, 1: {(3259, 5)}, 2: {(2549, 3)}, 3: set()}, 1583: {0: {(3041, 2)}, 1: {(2221, 7)}, 2: set(), 3: {(3121, 7)}}, 1861: {0: set(), 1: {(1427, 2)}, 2: {(1787, 0)}, 3: {(1889, 1)}}, 2099: {0: {(1181, 1)}, 1: {(3299, 0)}, 2: {(2281, 5)}, 3: {(1009, 1)}}, 2819: {0: {(3319, 1)}, 1: {(3761, 7)}, 2: {(2081, 0)}, 3: {(2833, 4)}}, 3803: {0: {(1009, 4)}, 1: set(), 2: {(3673, 4)}, 3: {(1181, 4)}}, 2803: {0: {(2357, 6)}, 1: {(3181, 2)}, 2: {(1493, 7)}, 3: {(2069, 4)}}, 1747: {0: {(2699, 0)}, 1: set(), 2: {(1847, 5)}, 3: {(3119, 4)}}, 2137: {0: {(2357, 4)}, 1: {(1543, 5)}, 2: {(2671, 7)}, 3: {(2857, 4)}}, 1847: {0: set(), 1: {(1747, 6)}, 2: {(3623, 2)}, 3: {(1453, 7)}}, 2381: {0: {(3347, 5)}, 1: {(2243, 0)}, 2: {(1091, 3)}, 3: {(3163, 6)}}, 3659: {0: {(3301, 3)}, 1: {(3673, 5)}, 2: {(1181, 7)}, 3: {(1103, 5)}}, 2207: {0: {(1931, 3)}, 1: {(2213, 5)}, 2: {(3761, 1)}, 3: {(3929, 0)}}, 2879: {0: {(1487, 0)}, 1: {(2677, 1)}, 2: {(1579, 5)}, 3: {(1901, 1)}}, 1321: {0: {(1451, 3)}, 1: {(3307, 1)}, 2: set(), 3: {(1571, 6)}}, 3331: {0: set(), 1: {(2593, 1)}, 2: {(3797, 6)}, 3: {(2221, 1)}}, 3623: {0: {(2711, 0)}, 1: {(3119, 7)}, 2: {(1847, 2)}, 3: {(1613, 3)}}, 3637: {0: {(1033, 0)}, 1: {(1543, 2)}, 2: {(2357, 7)}, 3: {(3181, 3)}}, 2677: {0: {(2417, 3)}, 1: {(2879, 1)}, 2: {(3019, 6)}, 3: {(3499, 5)}}, 3299: {0: {(2099, 1)}, 1: {(1013, 0)}, 2: {(2503, 1)}, 3: {(1933, 2)}}, 2647: {0: {(2351, 2)}, 1: {(3361, 5)}, 2: set(), 3: {(3967, 0)}}, 3943: {0: {(1231, 2)}, 1: {(3643, 2)}, 2: {(1283, 6)}, 3: {(2851, 4)}}, 2593: {0: set(), 1: {(3331, 1)}, 2: {(1979, 3)}, 3: {(1129, 2)}}, 3181: {0: {(3821, 3)}, 1: {(2963, 6)}, 2: {(2803, 1)}, 3: {(3637, 3)}}, 3697: {0: {(1741, 2)}, 1: {(2417, 4)}, 2: {(3499, 2)}, 3: {(3989, 4)}}, 1213: {0: {(2851, 2)}, 1: {(1327, 1)}, 2: {(2083, 4)}, 3: {(3631, 4)}}, 2053: {0: set(), 1: {(3121, 6)}, 2: {(3041, 3)}, 3: {(2297, 6)}}, 2549: {0: set(), 1: {(1381, 5)}, 2: {(1097, 3)}, 3: {(1481, 2)}}, 1451: {0: {(2281, 7)}, 1: {(2711, 7)}, 2: {(1613, 4)}, 3: {(1321, 0)}}, 1613: {0: {(1451, 6)}, 1: {(3307, 4)}, 2: {(1453, 0)}, 3: {(3623, 3)}}, 3301: {0: {(2683, 6)}, 1: {(2557, 5)}, 2: {(1607, 3)}, 3: {(3659, 0)}}, 1787: {0: {(1861, 2)}, 1: {(2017, 5)}, 2: {(2351, 5)}, 3: {(3361, 2)}}, 1051: {0: set(), 1: {(2861, 7)}, 2: {(2417, 1)}, 3: {(1741, 1)}}, 3041: {0: {(3163, 4)}, 1: {(2801, 7)}, 2: {(1583, 0)}, 3: {(2053, 2)}}, 3691: {0: {(3491, 6)}, 1: {(3049, 1)}, 2: {(2683, 0)}, 3: {(2161, 0)}}, 3319: {0: {(3877, 0)}, 1: {(2819, 0)}, 2: {(3671, 3)}, 3: set()}, 1381: {0: {(1597, 6)}, 1: {(2549, 5)}, 2: set(), 3: {(1129, 4)}}, 3673: {0: {(3803, 6)}, 1: {(3659, 5)}, 2: {(1607, 4)}, 3: set()}, 1493: {0: {(2963, 7)}, 1: {(2609, 2)}, 2: {(1061, 4)}, 3: {(2803, 6)}}, 1327: {0: {(2503, 4)}, 1: {(1213, 1)}, 2: {(3049, 7)}, 3: {(1933, 5)}}}
    # corners = [3121, 1889, 1187, 1789]
    # edges = [3347, 2297, 1129, 1607, 3307, 2467, 1427, 2213, 2699, 3253, 1201, 1571, 2861, 3361, 2789, 1453, 1741, 1523, 3671, 2221, 3967, 1993, 1009, 3877, 1481, 1583, 1861, 3803, 1747, 1847, 1321, 3331, 2647, 2593, 2053, 2549, 1051, 3319, 1381, 3673]
    # middle = [2609, 2801, 2851, 1237, 1931, 3989, 3491, 3931, 2011, 1033, 3761, 1277, 1487, 3617, 2017, 3119, 1933, 1597, 2351, 2243, 3163, 2281, 1097, 3821, 1231, 3631, 1913, 1013, 1181, 2671, 1721, 1877, 1091, 2161, 3079, 3797, 2311, 3259, 3019, 1979, 2287, 2437, 2833, 3929, 2711, 3511, 2417, 3727, 1061, 2389, 2113, 1283, 1901, 2357, 3529, 1039, 2963, 2557, 3049, 3719, 2069, 2083, 1103, 3643, 3499, 2503, 2729, 2129, 1217, 2339, 1579, 2683, 2777, 2081, 1543, 2857, 2099, 2819, 2803, 2137, 2381, 3659, 2207, 2879, 3623, 3637, 2677, 3299, 3943, 3181, 3697, 1213, 1451, 1613, 3301, 1787, 3041, 3691, 1493, 1327]

    # example matches
    matches = {2311: {0: {(1427, 2)}, 1: {(3079, 7)}, 2: set(), 3: {(1951, 1)}}, 1951: {0: {(2729, 2)}, 1: {(2311, 3)}, 2: set(), 3: set()}, 1171: {0: {(2473, 3)}, 1: {(1489, 5)}, 2: set(), 3: set()}, 1427: {0: {(1489, 2)}, 1: {(2473, 2)}, 2: {(2311, 0)}, 3: {(2729, 1)}}, 1489: {0: set(), 1: {(1171, 5)}, 2: {(1427, 0)}, 3: {(2971, 1)}}, 2473: {0: set(), 1: {(3079, 6)}, 2: {(1427, 1)}, 3: {(1171, 0)}}, 2971: {0: set(), 1: {(1489, 3)}, 2: {(2729, 0)}, 3: set()}, 2729: {0: {(2971, 2)}, 1: {(1427, 3)}, 2: {(1951, 0)}, 3: set()}, 3079: {0: set(), 1: set(), 2: {(2473, 5)}, 3: {(2311, 5)}}}
    corners =  [1951, 1171, 2971, 3079]
    edges = [2311, 1489, 2473, 2729]
    middle = [1427]
    print("matches", matches)


    # pick upper left corner
    for corner in corners:
        match = matches[corner]
        if len(match[1]) == len(match[2]) == 1:
            biggoGriddo[0][0] = corner
            tileGrid[0][0] = tiles[corner]
            break

    print(biggoGriddo)


    upperLeft = biggoGriddo[0][0]
    x, y = (0, 0)
    print("Upper left", upperLeft)
    # fill neighbors in both grids
    fillNeighbors(upperLeft, x, y, matches,tiles, biggoGriddo, tileGrid)

    b = np.fliplr(np.rot90(np.array(biggoGriddo), k=2))
    t = np.fliplr(np.rot90(np.array(tileGrid), k=2))
    print(b)

    # for row in t:
    #     for tile in row:
    #         print_2d_grid(tile)
    #         print()

    # one = t[0][0]
    # two = t[0][1]
    #
    # print_2d_grid(np.concatenate([one, two], axis=1))

    # print_2d_grid(t)
    resultGrid = tileGridToSingleGrid(t)
    print_2d_grid(resultGrid)

    # find and mark the dragons!
    part2_helpers.findSeaMonstersAndGetCount(resultGrid)

def tileGridToSingleGrid(tileGrid):
    grid = []
    for row in tileGrid:
        trimmedRow = []
        for tile in row:
            t1 = tile[1:-1, :] # remove first and last row
            t2 = t1[:, 1:-1] # remove first and las col
            trimmedRow.append(t2)
        newRow = np.concatenate(trimmedRow, axis=1)
        # newRow = np.concatenate(row, axis=1)
        grid.append(newRow)
    grid = np.concatenate(grid, axis=0)
    return grid

def fillNeighbors(tileNum, x, y, matches, tiles, biggoGriddo, tileGrid):
    # get current tile
    currentTile = tileGrid[y][x]
    # get this tile's matched tile ids
    matchingIds = getTileNumMatchingTileNums(tileNum, matches)
    print("matching ids", matchingIds)
    # for each 4 adj spots
    for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
        if 0 <= x2 < len(biggoGriddo[0]) and 0 <= y2 < len(biggoGriddo):
            nextItem = biggoGriddo[y2][x2]
            # if spot contains match, remove it
            if nextItem in matchingIds:
                matchingIds.remove(nextItem)
            elif nextItem is not None:
                print("RUH ROH")
                sys.exit(1)
            # if a spot is empty
            else:
                # for each unmatched tile id
                for matchingId in matchingIds:
                    # assume tile not already in the grid
                    # try each tile rotation here
                    tileRots = getTileConfigurations(tiles[matchingId])
                    foundMatch = False
                    for rot in tileRots:
                        # check if this tile fits, based on x,y,x2,y2
                        if checkFit(x,y,x2,y2,currentTile,rot):
                            biggoGriddo[y2][x2] = matchingId
                            tileGrid[y2][x2] = rot
                            fillNeighbors(matchingId, x2, y2, matches,tiles, biggoGriddo, tileGrid)
                            foundMatch = True
                            break
                    if foundMatch:
                        break

# orientations
# 0 - upright, no change        0 - top
# 1 - rotate left 90            1 - right
# 2 - rotate left 180           2 - bottom
# 3 - roate left 270            3 - left
# 4 - horizontal flip           4 - top flipped
# 5 - flipped rotate left 90    5 - right flipped
# 6 - flipped rotate left 180   6 - bottom flipped
# 7 - flipped rotat left 270    7 - left flipped


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
