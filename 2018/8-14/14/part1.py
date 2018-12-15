

def printBoard(board, firstElf, secondElf):
    for i in range(0, len(board)):
        score = board[i]
        if i == firstElf:
            print("(" + str(score) + ")", end=" ")
        elif i == secondElf:
            print("[" + str(score) + "]", end=" ")
        else:
            print(score, end=" ")
    print("")


def part1(numRecipes):
    board = [3, 7]
    firstElf = 0
    secondElf = 1

    printBoard(board, firstElf, secondElf)

    while len(board) < numRecipes + 10:
        firstScore = board[firstElf]
        secondScore = board[secondElf]
        newRecipe = firstScore + secondScore
        [board.append(int(c)) for c in str(newRecipe)]
        firstElf = firstElf + firstScore + 1
        secondElf = secondElf + secondScore + 1
        # print(firstElf, secondElf)
        if firstElf >= len(board):
            firstElf = firstElf % len(board)
        if secondElf >= len(board):
            secondElf = secondElf % len(board)
        # if secondElf == firstElf:
        #     secondElf += 1
        # print(firstElf, secondElf)
        # printBoard(board, firstElf, secondElf)
    lastTen = []
    for i in range(numRecipes, numRecipes+10):
        lastTen.append(board[i])
    for l in lastTen:
        print(str(l), end="")
    print("")
