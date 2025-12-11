import importlib
import time
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    days = []
    part1Times = []
    part2Times = []
    for i in range(1, 11):
        # if i in [5]:
        #     print("Skipping day", i)
        #     continue
        day = "{:02d}".format(i)
        days.append(day)
        print("Running day", day)

        importlib.invalidate_caches()
        module = importlib.import_module( f"..Day{day}", "src.subpkg")
        start = time.perf_counter()
        module.part1()
        end = time.perf_counter()
        total = (end-start) * 1000
        part1Times.append(total)

        start = time.perf_counter()
        module.part2()
        end = time.perf_counter()
        total = (end-start) * 1000
        part2Times.append(total)

    ind = np.arange(len(part1Times))
    width = 0.35
    plt.bar(ind, part1Times, width, label='Part 1')
    plt.bar(ind + width, part2Times, width, label='Part 2')

    plt.ylabel('Time (ms)')
    plt.title("AoC 2025` Times Python 3.9")

    plt.xticks(ind + width / 2, days)
    plt.legend(loc='best')
    plt.show()
