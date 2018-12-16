import networkx as nx
import string


def parseInput(input):
    pairs = []
    with open(input, 'r') as file:
        for line in file:
            s = line.strip().split(" ")
            first = (s[1])
            second = (s[7])
            pairs.append([first, second])
    return pairs


def solve(G):
    print(" ".join(nx.lexicographical_topological_sort(G)))


def createGraph(pairs):
    G = nx.DiGraph()
    for pair in pairs:
        G.add_edge(pair[0], pair[1])
    return G


def createDict(pairs, backwards=False):
    flatpairs = [item for sublist in pairs for item in sublist]
    deps = {}
    for pair in pairs:
        first = pair[0]
        second = pair[1]
        if backwards:
            first = pair[1]
            second = pair[0]
        if deps.get(first) is None:
            deps[first] = [second]
        else:
            deps[first].append(second)
    for uniq in flatpairs:
        if deps.get(uniq) is None:
            deps[uniq] = []
    return deps


def part2(filePath):
    # set up mapping of letters to time
    az = [c for c in string.ascii_uppercase]
    nums = [i+61 for i in range(0, 26)]
    timelookup = {}
    for i in range(0, 26):
        timelookup[az[i]] = nums[i]

    # the order to ultimately process everything in
    order = "ADEFKLBVJQWUXCNGORTMYSIHPZ"
    # order = "CABFDE"

    # read input, create dep dict
    pairs = parseInput(filePath)
    deps = createDict(pairs)
    # print(deps)

    # find which nodes we can start at
    revdeps = createDict(pairs, True)
    print(revdeps)
    queue = []
    for r in revdeps:
        if revdeps[r] == []:
            queue.append([r, timelookup[r], order.find(r)])
    # sort priority by order in toposort result
    queue = sorted(queue, key=lambda x: x[2])
    print("Q: " + str(queue))

    # set up workers
    numworkers = 5
    workers = [[None, 0] for i in range(0, numworkers)]

    inprogress = ""
    done = ""
    # init tasks
    for i in range(0, numworkers):
        if queue:
            workers[i] = queue.pop(0)
            inprogress += workers[i][0]
    print(workers)

    # schedule work
    time = 0
    someone_is_busy = True  # check if any worker is busy
    # continue while someone is busy and the queue is not empty
    while someone_is_busy or queue:
        someone_is_busy = False
        # check each worker
        for i in range(0, numworkers):
            worker = workers[i]

            # worker is not busy
            if worker[1] == 0:
                if queue:
                    workers[i] = queue.pop(0)
                    inprogress += workers[i][0]
                else:
                    workers[i] = [None, 0]

            # worker is about to finish something
            elif worker[1] == 1:
                # take thing they just finished and add to queue
                letter = worker[0]
                done += letter
                for dep in deps[letter]:
                    inqueue = False
                    for q in queue:
                        if q[0] == dep:
                            inqueue = True
                            break
                    prereqsdone = True
                    reqs = revdeps[dep]
                    for req in reqs:
                        if req not in done:
                            prereqsdone = False
                            break
                    if dep not in inprogress and dep not in done and not inqueue and prereqsdone:
                        queue.append([dep, timelookup[dep], order.find(dep)])
                queue = sorted(queue, key=lambda x: x[2])
                print("Q: " + str(queue))
                # assign new work
                if queue:
                    workers[i] = queue.pop(0)
                    inprogress += workers[i][0]
                    someone_is_busy = True
                else:
                    workers[i] = [worker[0], worker[1]-1, worker[2]]
                    someone_is_busy = True

            # worker is busy
            else:
                workers[i] = [worker[0], worker[1]-1, worker[2]]
                someone_is_busy = True
        print(str(workers) + "   " + done) # + "    " + inprogress)
        print("Q: " + str(queue))
        print("")

        # increment time
        time += 1
    print("time: " + str(time))
