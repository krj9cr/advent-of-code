
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


def part2(numRecipes):
    board = "37"
    firstElf = 0
    secondElf = 1

    # printBoard(board, firstElf, secondElf)
    recipeStr = str(numRecipes)

    while recipeStr not in board[-7:]:
        firstScore = int(board[firstElf])
        secondScore = int(board[secondElf])
        newRecipe = firstScore + secondScore
        board += str(newRecipe)
        # pick next recipe idx
        firstElf = firstElf + firstScore + 1
        secondElf = secondElf + secondScore + 1
        # loop around
        firstElf = firstElf % len(board)
        secondElf = secondElf % len(board)
    # printBoard(board, firstElf, secondElf)
    print(board.index(recipeStr))
