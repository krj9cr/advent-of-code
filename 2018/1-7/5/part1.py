import sys
import string

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " <input>")
    exit(1)

input = sys.argv[1]

line = ""
with open(input, 'r') as file:
    lines = []
    for line in file:
        str = line.strip()
        lines.append(str)

line = lines[0]


def detectReaction(str):
    for i in range(0, len(str)-1):
        c1 = str[i]
        c2 = str[i+1]
        if c1.lower() == c2.lower():
            if (c1.islower() and c2.isupper()) or (c1.isupper() and c2.islower()):
                return True
    return False


while detectReaction(line):
    for letter in string.ascii_lowercase:
        find1 = letter + letter.upper()
        find2 = letter.upper() + letter
        line = line.replace(find1, "")
        line = line.replace(find2, "")

print(len(line))
