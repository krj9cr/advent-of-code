import sys

if len(sys.argv) < 2:
    print "Usage: " + sys.argv[0] + " <input>"
    exit(1)

input = sys.argv[1]

with open(input, 'r') as file:
    # init
    lines = []
    freq = {0: 1}
    sum = 0
    for line in file:
        lines.append(int(line.strip()))

    repeat = True
    while (repeat):
        for num in lines:
            sum += num
            seen = freq.get(sum)
            if seen == None:
                freq[sum] = 1
            elif seen == 1:
                freq[sum] += 1
                repeat = False
                break
    print freq
    print "NUM: " + str(sum)
