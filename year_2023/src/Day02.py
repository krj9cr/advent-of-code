import sys
import time
import re

class Game:
    def __init__(self, gameId, num_rounds, rounds):
        self.gameId = gameId
        self.num_rounds = num_rounds
        self.rounds = rounds  # a list of rounds, where each round is a dict?

    def __str__(self):
        return "Game " + str(self.gameId) + ": " + str(self.rounds)

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        games = []
        for line in lines:
            gameId = re.findall(r'Game (\d+):', line)
            if len(gameId) < 1:
                print("Could not parse game id")
                sys.exit(1)
            gameId = int(gameId[0])
            # print(gameId)
            parts = line.split(": ")
            # print(parts)
            raw_rounds = parts[1].split(";")
            num_rounds = len(raw_rounds)
            rounds = []
            for raw_round in raw_rounds:
                cubes = raw_round.split(",")
                round_cubes = {}
                for cube in cubes:
                    cube_info = cube.strip().split(" ")
                    # print(cube_info)
                    num_cube = int(cube_info[0])
                    cube_color = cube_info[1]
                    round_cubes[cube_color] = num_cube
                rounds.append(round_cubes)
            games.append(Game(gameId, num_rounds, rounds))
            # print(rounds)
        return games

def part1():
    dayf = "{:02d}".format(2)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        max_red = 12
        max_green = 13
        max_blue = 14
        possible_games = []

        for line in file:
            line = line.strip()
            parts = line.split(": ")
            gameId = int(parts[0].strip("Game "))
            all_rounds_possible = True
            for raw_round in parts[1].split(";"):
                for cube in raw_round.split(","):
                    cube_info = cube.strip().split(" ")
                    num_cube = int(cube_info[0])
                    cube_color = cube_info[1]
                    if (cube_color == "red" and num_cube > max_red) or \
                            (cube_color == "green" and num_cube > max_green) or \
                            (cube_color == "blue" and num_cube > max_blue):
                        all_rounds_possible = False
                        break
                if not all_rounds_possible:
                    break
            if all_rounds_possible:
                possible_games.append(gameId)
        print(possible_games)
        print(sum(possible_games))

def part2():
    games = parseInput(2)
    power_sets = []
    for game in games:
        min_red = 0
        min_green = 0
        min_blue = 0
        for the_round in game.rounds:
            if the_round.get('red') is not None and the_round['red'] > min_red:
                min_red = the_round['red']
            if the_round.get('green') is not None and the_round['green'] > min_green:
                min_green = the_round['green']
            if the_round.get('blue') is not None and the_round['blue'] > min_blue:
                min_blue = the_round['blue']
        power_sets.append(min_red * min_green * min_blue)

    print(power_sets)
    print(sum(power_sets))

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    total = end - start
    print("Time (ms):", (end - start) * 1000)

    # print("\nPART 2 RESULT")
    # start = time.perf_counter()
    # part2()
    # end = time.perf_counter()
    # total = end - start
    # print("Time (ms):", (end - start) * 1000)
