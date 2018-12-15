import sys

if len(sys.argv) < 2:
    print "Usage: " + sys.argv[0] + " <input>"
    exit(1)

input = sys.argv[1]


# assumes strings are the same length
def compareTwoStrings(str1, str2):
    # append same characters to a string
    # length of this implies number of matching characters
    sameChars = ""
    for i in range(0, len(str1)):
        if str1[i] == str2[i]:
            sameChars += str1[i]
    # print str1, str2, sameChars
    return sameChars


def getLongestString(listOfStrings):
    max = 0
    longest = ""
    for str in listOfStrings:
        if len(str) > max:
            max = len(str)
            longest = str
    return longest


with open(input, 'r') as file:
    lines = []
    for line in file:
        str = line.strip()
        lines.append(str)
    counts = []
    for i in range(0, len(lines)):
        str1 = lines[i]
        for j in range(0, len(lines)):
            if i == j:
                continue
            count = compareTwoStrings(str1, lines[j])
            counts.append(count)
    # print counts
    longest = getLongestString(counts)
    print longest
