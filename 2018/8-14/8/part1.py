def parseInput(path):
    with open(path, 'r') as file:
        for line in file:
            return [int(num) for num in line.strip().split(" ")]


counter = 0
# expect 0 or at least 2 entries in nums list
def parseIntoTree(nums, tree, counter):
    counter += 1
    rest = nums[2:]
    numChild = nums[0]
    numMeta = nums[1]
    if numChild == 0:
        if numMeta == 0:
            tree[counter] = [{}, []]
            return rest
        else:
            tree[counter] = [{}, rest[:numMeta]]
            return rest[numMeta:]
    else:
        afterChild = rest
        children = {}
        for c in range(0, numChild):
            afterChild = parseIntoTree(afterChild, children, c)
        if numMeta == 0:
            tree[counter] = [children, []]
            return rest
        else:
            tree[counter] = [children, afterChild[:numMeta]]
            return afterChild[numMeta:]


def sumTree(tree):
    total = 0
    for t in tree:
        node = tree[t]
        children = node[0]
        metadata = node[1]
        print(t)
        print("   " + str(metadata))
        for meta in metadata:
            total += meta
        for child in children:
            total += sumTree(child)
    return total


def sumRoot(tree):
    total = 0
    print("TREE: ", tree)

    for t in tree:
        node = tree[t]
        children = node[0]
        metadata = node[1]
        if not children:
            for meta in metadata:
                total += meta
            return total
        else:
            print ("   ",children)
            for meta in metadata:
                child = children.get(meta)
                if child:
                    childsum = sumRoot({meta: child})
                    print(childsum)
                    total += childsum
            return total


def part1(path):
    lines = parseInput(path)
    tree = {}
    parseIntoTree(lines, tree, 0)
    print(tree)

    total = sumTree(tree)
    print(total)


def part2(path):
    lines = parseInput(path)
    tree = {}
    parseIntoTree(lines, tree, 0)
    print(tree)

    total = sumRoot(tree)
    print(total)
