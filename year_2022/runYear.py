import importlib
import time
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    days = []
    part1Times = []
    part2Times = []
    for i in range(1, 4):
        day = "{:02d}".format(i)
        days.append(day)

        module = __import__(f"Day{day}", fromlist=["src"])
        start = time.perf_counter()
        module.part1()
        end = time.perf_counter()
        total = end-start
        part1Times.append(total)

        start = time.perf_counter()
        module.part2()
        end = time.perf_counter()
        total = end-start
        part2Times.append(total)

    ind = np.arange(len(part1Times))
    width = 0.35
    plt.bar(ind, part1Times, width, label='Part 1')
    plt.bar(ind + width, part2Times, width, label='Part 2')

    plt.ylabel('Time')
    plt.title("AoC 2022 Times Python 3.9")

    plt.xticks(ind + width / 2, days)
    plt.legend(loc='best')
    plt.show()
