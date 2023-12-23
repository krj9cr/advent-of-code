import copy
import time

def get_min_height(points):
    return min([p[2] for p in points])

class Brick:
    def __init__(self, startPos, endPos):
        self.startPos = startPos  # 3 tuple: x, y ,z
        self.endPos = endPos      # 3 tuple: x, y ,z

        self.type = None  # "x", "y", or "z" for which way long it is

        # figure out how "long" bricks are, and store all their points
        # they are only long on one axis, it seems?
        self.points = []  # list of 3 tuples: x, y, z
        if self.startPos[0] != self.endPos[0]:
            if self.startPos[1] != self.endPos[1] or self.startPos[2] != self.endPos[2]:
                print("UH OH")
            else:
                self.type = "x"
                diff = abs(self.startPos[0] - self.endPos[0])
                rstart = min(startPos[0], endPos[0])
                for i in range(rstart, rstart + diff + 1):
                    self.points.append((i, startPos[1], startPos[2]))
        elif self.startPos[1] != self.endPos[1]:
            if self.startPos[0] != self.endPos[0] or self.startPos[2] != self.endPos[2]:
                print("UH OH")
            else:
                self.type = "y"
                diff = abs(self.startPos[1] - self.endPos[1])
                rstart = min(startPos[1], endPos[1])
                for i in range(rstart, rstart + diff + 1):
                    self.points.append((startPos[0], i, startPos[2]))
        elif self.startPos[2] != self.endPos[2]:
            if self.startPos[0] != self.endPos[0] or self.startPos[1] != self.endPos[1]:
                print("UH OH")
            else:
                self.type = "z"
                diff = abs(self.startPos[2] - self.endPos[2])
                rstart = min(startPos[2], endPos[2])
                for i in range(rstart, rstart + diff + 1):
                    self.points.append((startPos[0], startPos[1], i))
        if startPos == endPos:
            self.points.append(startPos)

        # get their min height (to sort by)
        self.minHeight = get_min_height(self.points)

    def __str__(self):
        return str(self.startPos) + " ~ " + str(self.endPos)

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        bricks = []
        for line in file:
            line = line.strip().split("~")
            startPos = [int(c) for c in line[0].split(",")]
            endPos = [int(c) for c in line[1].split(",")]
            bricks.append(Brick(startPos, endPos))
        return bricks

# updates 'bricks' array to make bricks fall
# 'check_if_fall' causes an early breakout
def bricks_fall(bricks, check_if_fall=False):
    fallen_bricks = copy.deepcopy(bricks)
    num_bricks = len(fallen_bricks)
    a_brick_fell = False
    for i in range(num_bricks):
        brick = fallen_bricks[i]
        # print(i, brick.minHeight, brick.points)
        if brick.minHeight == 1:
            continue
        # try to make the brick fall
        while True:
            # update its points
            fallen_points = [(p[0], p[1], p[2] - 1) for p in brick.points]
            # check for collisions against all other bricks
            collision = False
            for j in range(num_bricks):
                if i == j:
                    continue
                brick2 = fallen_bricks[j]
                for p in fallen_points:
                    if p in brick2.points:
                        collision = True
                        break
                if collision:
                    break
            if collision:
                break
            else:
                newMinHeight = get_min_height(fallen_points)
                # check for hitting the bottom
                if newMinHeight <= 0:
                    break
                # update the brick
                brick.points = fallen_points
                brick.minHeight = newMinHeight
                fallen_bricks[i] = brick
                a_brick_fell = True
                if check_if_fall:
                    return [], a_brick_fell
    return fallen_bricks, a_brick_fell


# simulates falling and checks how many bricks fell
def num_bricks_fall(bricks):
    fallen_bricks = copy.deepcopy(bricks)
    num_bricks = len(fallen_bricks)
    num_bricks_fell = 0
    for i in range(num_bricks):
        brick = fallen_bricks[i]
        # print(i, brick.minHeight, brick.points)
        if brick.minHeight == 1:
            continue
        brick_fell = False
        # try to make the brick fall
        while True:
            # update its points
            fallen_points = [(p[0], p[1], p[2] - 1) for p in brick.points]
            # check for collisions against all other bricks
            collision = False
            for j in range(num_bricks):
                if i == j:
                    continue
                brick2 = fallen_bricks[j]
                for p in fallen_points:
                    if p in brick2.points:
                        collision = True
                        break
                if collision:
                    break
            if collision:
                break
            else:
                newMinHeight = get_min_height(fallen_points)
                # check for hitting the bottom
                if newMinHeight <= 0:
                    break
                # update the brick
                brick.points = fallen_points
                brick.minHeight = newMinHeight
                fallen_bricks[i] = brick
                brick_fell = True
        if brick_fell:
            num_bricks_fell += 1
    return num_bricks_fell

def part1():
    bricks = parseInput(22)
    # sort bricks by minHeight
    bricks = sorted(bricks, key=lambda b: b.minHeight)

    num_bricks = len(bricks)

    # make bricks "fall"
    bricks, _ = bricks_fall(bricks)

    # print for debugging
    # print("Fallen:")
    # for i in range(num_bricks):
    #     brick = bricks[i]
    #     print(i, brick.minHeight, brick.points)

    # sort bricks by minHeight again
    bricks = sorted(bricks, key=lambda b: b.minHeight)
    # check if each brick can be disintegrated
    disintegrate_count = 0
    for i in range(num_bricks):
        brick = bricks[i]
        print(i, brick.minHeight, brick.points)
        # remove the brick
        # bricks_removed = bricks[:i] + bricks[i+1:]
        # remove the brick, also only keep higher bricks
        bricks_removed = bricks[:i] + bricks[i+1:]
        # simulate falling again
        _, a_brick_fell = bricks_fall(bricks_removed, check_if_fall=True)
        if a_brick_fell:
            continue
        else:
            disintegrate_count += 1
    print(disintegrate_count)

def part2():
    bricks = parseInput(22)
    # sort bricks by minHeight
    bricks = sorted(bricks, key=lambda b: b.minHeight)

    num_bricks = len(bricks)

    # make bricks "fall"
    bricks, _ = bricks_fall(bricks)

    # print for debugging
    print("Fallen")
    # for i in range(num_bricks):
    #     brick = bricks[i]
    #     print(i, brick.minHeight, brick.points)

    # sort bricks by minHeight again
    bricks = sorted(bricks, key=lambda b: b.minHeight)
    # check if each brick can be disintegrated
    answer = 0
    for i in range(num_bricks):
        brick = bricks[i]
        # remove the brick
        # bricks_removed = bricks[:i] + bricks[i+1:]
        # remove the brick, also only keep higher bricks
        bricks_removed = bricks[:i] + bricks[i+1:]
        # simulate falling again
        # TODO: could probably do some kind of caching to improve performance
        #       like keep track of "if brick A falls, then 12 bricks fall" and be able to look that up
        num_bricks_fell = num_bricks_fall(bricks_removed)
        print(i, brick.points, "fell:", num_bricks_fell)
        answer += num_bricks_fell
    print(answer)

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
