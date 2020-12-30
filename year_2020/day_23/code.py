import time

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return "Node(" + str(self.data) + ") -> " + str(self.next.data)

def move_three_nodes_after_to(from_after_node, to_after_node):
    # remove
    one = from_after_node.next
    three = one.next.next
    from_after_node.next = three.next
    # add
    prev = to_after_node.next
    to_after_node.next = one
    three.next = prev

# A "smart" circular linked list
# https://www.javatpoint.com/python-program-to-create-and-display-a-circular-linked-list
class CircularLinkedList:
    def __init__(self, nodes=None):
        self.head = None
        # a dict of data -> node
        # helps with faster lookups for extremely long chains
        self.nodePointers = {}
        if nodes is not None:
            elem = nodes.pop(0)
            node = Node(data=elem)
            self.nodePointers[elem] = node
            self.head = node
            for elem in nodes:
                n = Node(data=elem)
                node.next = n
                self.nodePointers[elem] = n
                node = node.next
            node.next = self.head

    # assumes list is not empty
    # return the last cup
    def append(self, nodes):
        # find last node
        node = None
        for n in self:
            node = n
        for elem in nodes:
            n = Node(data=elem)
            node.next = n
            self.nodePointers[elem] = n
            node = node.next
        node.next = self.head
        return node

    # This function will add the new node at the end of the list.
    def add(self, data):
        newNode = Node(data)
        self.nodePointers[data] = newNode
        # Checks if the list is empty.
        if self.head is None:
            # If list is empty, the head will be the new node.
            self.head = newNode
            newNode.next = self.head
        else:
            node = None
            for n in self:
                node = n
            node.next = newNode
            newNode.next = self.head

    # Displays all the nodes in the list
    def display(self):
        current = self.head
        if not self.head:
            raise Exception("List is empty")
        else:
            print("Nodes of the circular linked list: ")
            #Prints each node by incrementing pointer.
            print(current.data),
            while current.next != self.head:
                current = current.next
                print(current.data),

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next
            if node == self.head:
                break

    def __repr__(self):
        nodes = []
        for node in self:
            nodes.append(str(node.data))
        return " -> ".join(nodes)

    # assume list is not empty
    def find(self, target_node_data):
        # if not self.head:
        #     raise Exception("List is empty")
        # try to lookup
        node = self.nodePointers.get(target_node_data)
        if node is not None:
            return node
        # otherwise hunt for it SLOWLY
        for node in self:
            if node.data == target_node_data:
                return node
        raise Exception("Node with data '%s' not found" % target_node_data)

    def move(self, lenCups, prevCup, currentCup):
        # self.head = currentCup
        pickup1 = currentCup.next
        pickup2 = pickup1.next
        pickup3 = pickup2.next

        # destination cup: the cup with a label equal to the current cup's label minus one
        destinationCup = currentCup.data - 1
        # If this would select one of the cups that was just picked up,
        # the crab will keep subtracting one until it finds a cup that wasn't just picked up
        while destinationCup == pickup1.data or destinationCup == pickup2.data or destinationCup == pickup3.data:
            destinationCup -= 1
        # If at any point in this process the value goes below the lowest value on any cup's label,
        # it wraps around to the highest value on any cup's label instead
        if destinationCup < 1:
            destinationCup = lenCups
        while destinationCup == pickup1.data or destinationCup == pickup2.data or destinationCup == pickup3.data:
            destinationCup -= 1
        # print("desintation:", destinationCup)

        # move picked up cups after destination cup
        destinationNode = prevCup
        if prevCup.data != destinationCup:
            destinationNode = self.find(destinationCup)
        move_three_nodes_after_to(currentCup, destinationNode)


        currentCup = currentCup.next

        return currentCup

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file][0]

def parseLine(line: str):
    return [ int(s) for s in line.strip() ]

def getLabelsAfterOne(cups):
    oneNode = cups.find(1)
    cups.head = oneNode
    l = []
    for node in cups:
        l.append(str(node.data))
    l.pop(0) # remove one
    return "".join(l)


###########################
# part1
###########################
def part1(data):
    m = max(data)
    numCups = len(data)
    # numCups = 1000000
    cups = CircularLinkedList(data[:])
    prevCup = cups.append(range(m+1, numCups+1))

    print("cups:", cups)
    currentCup = cups.head
    # numMoves = numCups
    numMoves = 100
    for i in range(numMoves):
        print("move ", i)
        newCup = cups.move(cups, numCups, prevCup, currentCup)
        prevCup = currentCup
        currentCup = newCup
        print("current cup:", currentCup)
        # print("cups:", cups)
        print()

    print("Final cups", cups)
    res = getLabelsAfterOne(cups)
    print("result", res)



def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def getTwoCupsAfterOne(cups):
    oneNode = cups.find(1)
    val1 = oneNode.next
    val2 = val1.next
    print("vals",val1.data, val2.data)
    return val1.data * val2.data

def part2(data):
    m = max(data)
    numCups = 1000000 # one million
    cups = CircularLinkedList(data[:])
    prevCup = cups.append(range(m+1, numCups+1))

    currentCup = cups.head
    numMoves = 10000000 # ten million
    for i in range(numMoves):
        # print("move ", i)
        newCup = cups.move(numCups, prevCup, currentCup)
        prevCup = currentCup
        currentCup = newCup

    # print("Final cups", cups)
    res = getTwoCupsAfterOne(cups)
    print("result", res)

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
