import sys


# def get_input():
#     if len(sys.argv) < 2:
#         print "Usage: " + sys.argv[0] + " <input>"
#         exit(1)
#
#     return sys.argv[1]


def get_lines(path):
    with open(path, 'r') as f:
        return [line.strip() for line in f]


