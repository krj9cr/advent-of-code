def countLetters(str):
    counts = {}
    # put letters in dictionary
    for char in str:
        if counts.get(char) == None:
            counts[char] = 1
        else:
            counts[char] += 1
    # check if any letter was seen 2 or 3 times
    num2 = 0
    num3 = 0
    for char in counts:
        if counts[char] == 2:
            num2 = 1
        elif counts[char] == 3:
            num3 = 1
    return [num2, num3]


def sumAndMult(listOfCounts):
    num2 = 0
    num3 = 0
    for pair in listOfCounts:
        num2 += pair[0]
        num3 += pair[1]
    return num2 * num3


def part1(path: str):
    with open(path, 'r') as file:
        counts = []
        for line in file:
            str = line.strip()
            strCount = countLetters(str)
            counts.append(strCount)
            # print(str, strCount)
        value = sumAndMult(counts)
        print(value)
