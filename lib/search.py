from collections import deque

# grid   - a 2d array of strings or numbers
# start   - a tuple of numbers representing the starting coordinate in the 2d grid
# end     - a tuple of numbers representing the ending coordinate in the 2d grid
# include - characters allowed to traverse, e.g. "."
# exclude - characters not allowed to traverse, e.g. "#"
def bfs_2d_grid(grid, start, end, include="", exclude=""):
    queue = deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == end:
            return path
        for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
                next = (x2, y2)
                nextItem = grid[y2][x2]
                if next not in seen and \
                        (include == "" or nextItem in include) and \
                        (exclude == "" or nextItem not in exclude):
                    queue.append(path + [next])
                    seen.add(next)

# map     - a dict of coordinate tuples to values in the map, for example:
#           { (2,2): "#", (2,1): "." }
#           this allows for better storage of sparse maps, or only storing open or known coordinates
# start   - a tuple of numbers representing the starting coordinate in the 2d grid
# end     - a tuple of numbers representing the ending coordinate in the 2d grid
# include - characters allowed to traverse, e.g. "."
# exclude - characters not allowed to traverse, e.g. "#"
def bfs_2d_map(map, start, end, include="", exclude=""):
    queue = deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == end:
            return path
        for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            next = (x2, y2)
            nextItem = map[(x2, y2)]
            if next not in seen and \
                    (include == "" or nextItem in include) and \
                    (exclude == "" or nextItem not in exclude):
                queue.append(path + [next])
                seen.add(next)
