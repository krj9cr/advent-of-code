
class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.data) + "\n"
        for child in (self.left, self.right):
            if child:
                ret += child.__str__(level + 1)
        return ret

    def traverse(self):
        thislevel = [self]
        a = '                                 '
        while thislevel:
            nextlevel = list()
            a = a[:int(len(a) / 2)]
            for n in thislevel:
                print(a + str(n.data), end="")
                if n.left:
                    nextlevel.append(n.left)
                if n.right:
                    nextlevel.append(n.right)
                thislevel = nextlevel
            print("")


def parseInput(path: str):
    with open(path, 'r') as file:
        return file.readline().strip("^").strip("$")


# assumes input is a string like "(asdf...)..."
def findGroup(line: str):
    if line[0] == "(":
        openBr = 1
        end = 1
        for i in range(1, len(line)):
            if line[i] == "(":
                openBr += 1
            elif line[i] == ")":
                openBr = openBr - 1
            if openBr == 0:
                end = i
                break
        return line[1:end]
    else:
        print("bad input for findGroup")
        exit(1)


def buildTree(line: str):
    if not line:
        return None
    nextGroup = line.find("(")
    thisNode = Tree()
    # No more groups
    if nextGroup == -1:
        thisNode.data = line
        return thisNode
    else:
        thisNode.data = line[:nextGroup]
        group = findGroup(line[nextGroup:])
        thisNode.left = buildTree(group)
    return thisNode


def move(spots, line: str):
    print(line)
    x, y = spots[-1]
    for l in line:
        if l == "N":
            (x, y) = (x, y - 1)
            spots.append((x, y))
        elif l == "W":
            (x, y) = (x - 1, y)
            spots.append((x, y))
        elif l == "E":
            (x, y) = (x + 1, y)
            spots.append((x, y))
        elif l == "S":
            (x, y) = (x, y + 1)
            spots.append((x, y))
        else:
            print("bad input for move")
            exit(1)
    return spots


def followPath(spots, line: str):
    if not line:
        return None
    nextGroup = line.find("(")
    nextBranch = line.find("|")
    # No more branches or groups
    if nextBranch == -1 and nextGroup == -1:
        spots += (move(spots, line))
    # Have both a branch and a group
    elif nextGroup != -1 and nextBranch != -1:
        # Group is first
        if nextGroup < nextBranch:
            spots += (move(spots, line[:nextGroup]))
            group = findGroup(line[nextGroup:])
            spots = followPath(spots, group)
        # Branch is first
        else:
            spots += (move(spots, line[:nextGroup]))
            spots = followPath(spots, line[:nextBranch])
            spots = followPath(spots, line[nextBranch+1:])
    # Only one, probably a branch
    elif nextBranch != -1:
        spots = followPath(spots, line[:nextBranch])
        spots = followPath(spots, line[nextBranch + 1:])
    else:
        print("idk")
        exit(1)
    return spots


def part1(path: str):
    line = parseInput(path)
    print(line)

    tree = buildTree(line)
    tree.traverse()
    # spots = [(0, 0)]
    # spots = followPath(spots, line)
    # print(spots)


def part2(path: str):
    lines = parseInput(path)
    print(lines)
