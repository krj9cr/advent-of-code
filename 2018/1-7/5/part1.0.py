import sys

if len(sys.argv) < 2:
  print("Usage: " + sys.argv[0] + " <input>")
  exit(1)

input = ""
with open(sys.argv[1], 'r') as file:
  # only read one line
  input = file.readlines()[0].strip()
  #print(input)


def find_and_remove_pair(input):
  result = ""
  i = 0
  while i < len(input):
    c1 = input[i]
    if i+1 >= len(input):
      result += c1
      break
    c2 = input[i+1]
    if willReact(c1, c2):
      i += 1
    else:
      result += c1
    i += 1
    #print(result)
  if result == input:
    return result
  return find_and_remove_pair(result)

def willReact(c1, c2):
  if (c1.lower() == c2.lower()):
    if (c1.islower() and c2.isupper()) or (c1.isupper() and c2.islower()):
      return True
  return False

print(find_and_remove_pair(input))
