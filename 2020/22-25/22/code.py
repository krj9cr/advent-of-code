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
        print(nextPlayer1, nextPlayer2)
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

def playRound(player1, player2):
    p1card = player1[0]
    p2card = player2[0]

    # check if we should recurse
    if len(player1)-1 >= p1card and len(player2)-1 >= p2card:
        winner, player = playGame(player1[1:], player2[1:])
        if player == 1:
            newPlayer1 = player1[1:] + [p1card, p2card]
            newPlayer2 = player2[1:]
        elif player == 2:
            newPlayer2 = player2[1:] + [p2card,p1card]
            newPlayer1 = player1[1:]
        else:
            print("I messed up")
            sys.exit()
        return newPlayer1, newPlayer2
    else:
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

def playGame(player1, player2):
    nextPlayer1 = deepcopy(player1)
    nextPlayer2 = deepcopy(player2)

    # keep track of hands
    memory = {1: set(), 2: set() }

    # print("wtf",memory)

    winner = None
    i = 0
    while winner is None:
        # add hands to memory
        memory[1].add(handToString(nextPlayer1))
        memory[2].add(handToString(nextPlayer2))

        # print("Round", i)
        # print(nextPlayer1, nextPlayer2)
        nextPlayer1, nextPlayer2 = playRound(nextPlayer1, nextPlayer2)


        # check normal win condition
        if len(nextPlayer1) == 0:
            winner = (nextPlayer2, 2)
        if len(nextPlayer2) == 0:
            winner = (nextPlayer1, 1)
        i += 1

        # print("memory",memory)
        # check infinite loop condition
        if handToString(nextPlayer1) in memory[1] and handToString(nextPlayer2) in memory[2]:
            winner = (nextPlayer1, 1)
            return winner


    return winner

def part2(data):
    # print(data)

    player1 = data[0]
    player2 = data[1]

    winner, player = playGame(player1, player2)

    print("player",player, "wins it all! with", winner)
    getWinnerScore(winner)



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
