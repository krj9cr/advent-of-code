import importlib
import time
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    days = []
    part1Times = []
    part2Times = []
    for i in range(1, 20):
        if i == 11:
            continue
        day = "{:02d}".format(i)
        days.append(day)

        module = importlib.import_module(f"year_2020.day_{day}.code")

        start = time.perf_counter()
        module.runpart1()
        end = time.perf_counter()
        total = end-start
        part1Times.append(total)

        start = time.perf_counter()
        module.runpart2()
        end = time.perf_counter()
        total = end-start
        part2Times.append(total)

    ind = np.arange(len(part1Times))
    width = 0.35
    plt.bar(ind, part1Times, width, label='Part 1')
    plt.bar(ind + width, part2Times, width, label='Part 2')

    plt.ylabel('Time')
    plt.title("AoC 2020 Times Python 3.8")

    plt.xticks(ind + width / 2, days)
    plt.legend(loc='best')
    plt.show()
