import time
import sys
from copy import deepcopy

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
                batchedlines.append(currBatch)
                currBatch = []
        batchedlines.append(currBatch)

        res = []
        for batch in batchedlines:
            res.append([ int(b) for b in batch[1:]])
        return res

def parseLine(line: str):
    return line.strip()

def doRound(player1, player2):
    p1card = player1[0]
    p2card = player2[0]
    if p1card > p2card:
        newPlayer1 = player1[1:] + [p1card, p2card]
        newPlayer2 = player2[1:]
    else:
        newPlayer2 = player2[1:] + [p2card,p1card]
        newPlayer1 = player1[1:]
    return newPlayer1, newPlayer2

def getWinnerScore(winner):
    res = 0
    for w in range(len(winner)):
        # print(winner[w], "*", len(winner)-w)
        res += ((len(winner)-w) * winner[w])
    print("result",res)

###########################
# part1
###########################
def part1(data):
    # print(data)

    player1 = data[0]
    player2 = data[1]


    nextPlayer1 = deepcopy(player1)
    nextPlayer2 = deepcopy(player2)

    winner = None
    i = 0
    while winner is None:
        print("Round", i)
        print(nextPlayer1)
        print(nextPlayer2)
        nextPlayer1, nextPlayer2 = doRound(nextPlayer1, nextPlayer2)
        if len(nextPlayer1) == 0:
            print("Player 2 wins!")
            winner = nextPlayer2
        if len(nextPlayer2) == 0:
            print("Player 1 wins!")
            winner = nextPlayer1
        i += 1

    print("winner",winner)

    getWinnerScore(winner)


def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################

def playRound(player1, player2, gi):
    p1len = len(player1)
    p2len = len(player2)
    # check if either player is empty
    # if p1len == 0 or p2len == 0:
    #     return player1, player2

    p1card = player1[0]
    p2card = player2[0]

    # check if we should recurse
    if p1len-1 >= p1card and p2len-1 >= p2card:
        # end1 = min(1 + p1card, p1len)
        # end2 = min(1 + p2card, p2len)
        next1 = player1[1:][:p1card]
        next2 = player2[1:][:p2card]
        _, player = playGame(deepcopy(next1), deepcopy(next2), gi + 1)
        if player == 1:
            newPlayer1 = player1[1:] + [p1card, p2card]
            newPlayer2 = player2[1:]
        elif player == 2:
            newPlayer2 = player2[1:] + [p2card, p1card]
            newPlayer1 = player1[1:]
        else:
            print("I messed up")
            sys.exit()
        return newPlayer1, newPlayer2

    # normal round
    if p1card > p2card:
        newPlayer1 = player1[1:] + [p1card, p2card]
        newPlayer2 = player2[1:]
    else:
        newPlayer2 = player2[1:] + [p2card,p1card]
        newPlayer1 = player1[1:]
    return newPlayer1, newPlayer2

def handToString(hand):
    return ",".join([ str(num) for num in deepcopy(hand) ])

def playGame(p1, p2, gi):
    player1 = deepcopy(p1)
    player2 = deepcopy(p2)
    # check normal win condition upfront in case one is empty
    if len(player1) == 0:
        return player2, 2
    if len(player2) == 0:
        return player1, 1

    # shortcut, if p1 has the max card they win
    if gi != 0:
        m = max(player1 + player2)
        if m in player1:
            return player1, 1

    # keep track of hands
    memory = {1: [], 2: []}
    # add curr hands to memory

    winner = None
    i = 0
    while winner is None:

        lastp1 = deepcopy(player1)
        lastp2 = deepcopy(player2)

        # check infinite loop condition
        s1 = handToString(player1)
        s2 = handToString(player2)
        if s1 in memory[1] or s2 in memory[2]:
            return player1, 1

        # check normal win condition
        if len(player1) == 0:
            return player2, 2
        if len(player2) == 0:
            return player1, 1

        print("Game", gi, "Round", i)
        print(player1, player2)
        player1, player2 = playRound(player1, player2, gi)

        # add curr hands to memory
        memory[1].append(handToString(lastp1))
        memory[2].append(handToString(lastp2))

        i += 1

    return winner

def part2(data):
    # print(data)

    player1 = data[0]
    player2 = data[1]

    origlen1 = len(player1) + len(player2)

    gi = 0
    winner, player = playGame(player1, player2, gi)

    print("player",player, "wins it all! with", winner)
    getWinnerScore(winner)
    # print("original len",origlen1, "final len", len(winner))
    for i in range(1, len(winner)+1):
        if i not in winner:
            print("OH NO missing", i)

# 8952 too low
# 32244 no
# 32425 too high
# 33501 too high
# 34299 no
# 34472 lol no

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
