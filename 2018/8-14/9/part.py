from collections import deque, defaultdict


def part1(numPlayers, lowestMarble, highestMarble):
    print("numPlayers:", numPlayers, "highestMarble:", highestMarble)
    circle = [lowestMarble]
    playerScores = {}
    for i in range(0, numPlayers):
        playerScores[i+1] = 0
    # print(playerScores)
    player = 1
    currentMarble = lowestMarble
    nextMarble = lowestMarble + 1
    while nextMarble <= highestMarble:
        # turn
        currentMarbleIndex = circle.index(currentMarble)

        # special turn
        # where the player gets points
        if nextMarble % 23 == 0:
            # get and remove the marble 7 left from currentMarble
            removeIndex = currentMarbleIndex - 7
            if removeIndex < 0:
                removeIndex = len(circle) + removeIndex
            # print(nextMarble, currentMarble, removeIndex)
            number = circle[removeIndex]
            playerScores[player] += nextMarble + number
            print(nextMarble, number)
            circle = circle[:removeIndex] + circle[removeIndex+1:]
            currentMarble = circle[removeIndex]
        # regular turn
        # insert marble between next two in circle (wrap around)
        else:
            before = currentMarbleIndex + 1
            after = currentMarbleIndex + 2
            # check bounds
            if currentMarbleIndex == len(circle) - 2:
                circle.append(nextMarble)
            elif currentMarbleIndex == len(circle) - 1:
                before = 0
                after = 1
                # add marble between before and after marble locations
                circle = circle[:before + 1] + [nextMarble] + circle[after:]
            else:
                # add marble between before and after marble locations
                circle = circle[:before + 1] + [nextMarble] + circle[after:]
            currentMarble = nextMarble

        # increment infos
        if (player == numPlayers):
            player = 1
        else:
            player += 1
        nextMarble += 1
        # print(circle)
    # print(playerScores)
    winningPlayer = max(playerScores, key=lambda x: playerScores[x])
    print(playerScores[winningPlayer])


def part2(numPlayers, highestMarble):
    scores = defaultdict(int)
    circle = deque([0])

    for marble in range(1, highestMarble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % numPlayers] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    win = max(scores.values()) if scores else 0
    print(win)
