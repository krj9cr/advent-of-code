import time

class Node:
    def __init__(self, data=None, is_dir=False, children=None, parent=None):
        self.is_dir = is_dir
        self.data = data
        self.size = 0
        if children:
            self.children = children # list of Nodes
        else:
            self.children = []
        self.parent = parent

    # def __repr__(self):
    #     return "Node(" + str(self.data) + ") -> " + str(self.child.data)

    def __repr__(self, level=0):
        ret = "\t"*level + repr(self.data) + ": " + repr(self.size) + "\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret


def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        return lines

def getSums(node):
    size = node.size
    for child in node.children:
        size += getSums(child)
    node.size = size
    return size

def getAnswer(node):
    answer = 0
    if node.size <= 100000:
        answer += node.size
    for child in node.children:
        answer += getAnswer(child)
    return answer

def part1():
    lines = parseInput(7)[1:] # skip the first line since it's root dir
    print(lines)
    root = Node(data="/", is_dir=True)
    currNode = root
    for line in lines:
        # command
        if line.startswith("$"):
            split = line.split(" ")[1:]
            command = split[0]
            if command == "cd":
                dir = split[1]
                print(command, dir)
                if dir == "..":
                    currNode = currNode.parent
                else:
                    # check if child already exists
                    exists = False
                    if currNode.children is not None:
                        for child in currNode.children:
                            if child.data == dir:
                                currNode = child
                                exists = True
                    if not exists:
                        newNode = Node(data=dir, is_dir=True, parent=currNode)
                        currNode.children.append(newNode)
                        currNode = newNode

            elif command == "ls":
                # print(command)
                True # can ignore since we'll just parse the output
        # output
        else:
            # print(line)
            split = line.split(" ")
            first = split[0]
            if first == "dir":
                continue # OR make the node as a child but don't move to it?
            else: # it's a file
                print("Adding ", int(first), "to ", currNode.data)
                currNode.size += int(first)
    getSums(root)
    print(root)
    print(getAnswer(root))
    return root

# choose a directory, where the size is greater than min_need_to_free_space, but minimizing the diff
def part2Answer(node, currNode, min_space, min_diff=99999999):
    if node.is_dir:
        # diff = node.size - min_space
        if min_space <= node.size < currNode.size:
            currNode = node
            # min_diff = diff
        for child in node.children:
            currNode = part2Answer(child, currNode, min_space, min_diff)
    return currNode

def part2():
    # lines = parseInput(7)
    # print(lines)
    root = part1()
    total_space = 70000000
    required_unused_space = 30000000
    # root.size = 48381165
    unused_space = total_space - root.size
    min_need_to_free_space = required_unused_space - unused_space
    print(min_need_to_free_space)
    # choose a directory, where the size is greater than min_need_to_free_space, but minimizing the diff
    answer = part2Answer(root, root, min_need_to_free_space)
    print(answer.data, answer.size)

# 98693 too low

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
