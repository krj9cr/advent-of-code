import time
from collections import OrderedDict



def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append(line)
        return lines[0]

def part1():
    line = parseInput(9)
    blocks = []
    storage = []
    num_free_spots = 0
    for i in range(len(line)):
        size = int(line[i])
        if i % 2 == 0:
            id = int((i/2))
            for j in range(size):
                storage.append(id)
        else:
            num_free_spots += 1
            for j in range(size):
                storage.append(".")
    # print(storage)
    total_size = len(storage)

    # find first free spot
    free_idx = 0
    for i in range(total_size):
        item = storage[i]
        if item == ".":
            free_idx = i
            break
    # print(free_idx)
    # print(num_free_spots)

    # find last file spot
    file_idx = total_size - 1
    for i in range(file_idx, -1, -1):
        item = storage[i]
        if item != ".":
            file_idx = i
            break
    # print(file_idx)

    count = 0
    while True:
        storage[free_idx] = storage[file_idx]
        storage[file_idx] = "."

        # find next free spot
        for i in range(free_idx + 1, total_size):
            item = storage[i]
            if item == ".":
                free_idx = i
                break

        # find next file spot
        for i in range(file_idx - 1, -1, -1):
            item = storage[i]
            if item != ".":
                file_idx = i
                break
        # print(free_idx, file_idx)

        # print(storage)
        count += 1
        # if count > 10:
        #     break
        if free_idx > file_idx:
            break

    # get answer
    total = 0
    for i in range(total_size):
        item = storage[i]
        if item != ".":
            total += i * storage[i]
        else:
            break
    print(total)




def part2():
    line = parseInput(9)
    blocks = []
    storage = []
    files = OrderedDict()
    free_space = OrderedDict()
    num_free_spots = 0
    # create storage array
    for i in range(len(line)):
        size = int(line[i])
        if i % 2 == 0:
            id = int((i / 2))
            files[id] = (size, len(storage))
            for j in range(size):
                storage.append(id)
        else:
            num_free_spots += 1
            free_space[len(storage)] = size
            for j in range(size):
                storage.append(".")
    print(storage)
    total_size = len(storage)
    print("total size", total_size)
    # print(files)
    # print(free_space)


    # find first free spot and how big it is
    free_idx = 0
    free_spots = 0
    found_free = False
    for i in range(total_size):
        item = storage[i]
        if not found_free and item == ".":
            free_idx = i
            found_free = True
        if found_free:
            if item == ".":
                free_spots += 1
            else:
                break
    print("next free idx", free_idx, "free_spots", free_spots)

    # find last file spot, and how big it is
    # file_idx = total_size - 1
    # file_size = 0
    # found_file = False
    # file_num = 0
    # for i in range(file_idx, -1, -1):
    #     item = storage[i]
    #     if not found_file and item != ".":
    #         file_idx = i
    #         found_file = True
    #         file_num = item
    #     if found_file:
    #         if item == file_num:
    #             file_size += 1
    #             file_idx = i
    #         else:
    #             break
    # print("file_num", file_num, "file index:", file_idx, "file_Size", file_size)

    # find last file spot, and how big it is
    curr_file = files.popitem(last=True)
    print(curr_file)
    print(free_space)
    file_idx = curr_file[1][1]
    file_size = curr_file[1][0]
    file_num = curr_file[0]
    print("file_num", file_num, "file index:", file_idx, "file_Size", file_size)

    count = 0
    while True:
        if file_size == 0:
            curr_file = files.popitem(last=True)
            file_idx = curr_file[1][1]
            file_size = curr_file[1][0]
            file_num = curr_file[0]
            # print(curr_file, files)
            # print("file_num", file_num, "file index:", file_idx, "file_Size", file_size)

        if file_size <= free_spots and free_idx < file_idx:
            print("MOVING ITEM", file_num)
            # move da file wholly
            storage[free_idx:free_idx+file_size] = [file_num] * file_size
            storage[file_idx:file_idx+file_size] = ["."] * file_size

            # find last file spot, and how big it is
            if len(files) <= 1:
                break
            curr_file = files.popitem(last=True)
            file_idx = curr_file[1][1]
            file_size = curr_file[1][0]
            file_num = curr_file[0]
            # print(curr_file, files)
            # print("file_num", file_num, "file index:", file_idx, "file_Size", file_size)

            # find first free spot
            free_idx = 0
            free_spots = 0
            found_free = False
            for i in range(0, total_size):
                item = storage[i]
                if not found_free and item == ".":
                    free_idx = i
                    found_free = True
                if found_free:
                    if item == ".":
                        free_spots += 1
                    else:
                        break
            # print("next free idx", free_idx, "free_spots", free_spots)
            # print(storage)
            # print()
        else:
            # the file won't fit in this free spot
            # find next free spot
            prev_size = free_spots
            free_spots = 0
            found_free = False
            for i in range(free_idx+prev_size, total_size):
                item = storage[i]
                if not found_free and item == ".":
                    free_idx = i
                    found_free = True
                if found_free:
                    if item == ".":
                        free_spots += 1
                    else:
                        break
            # print("file_num", file_num, "file index:", file_idx, "file_Size", file_size)
            # print("next free idx", free_idx, "free_spots", free_spots)

            # couldn't find a spot for this file, so move on
            if free_idx >= file_idx:
                print("MOVING ON")
                # find last file spot, and how big it is
                if len(files) <= 1:
                    break
                curr_file = files.popitem(last=True)
                file_idx = curr_file[1][1]
                file_size = curr_file[1][0]
                file_num = curr_file[0]
                # print(curr_file, files)
                # print("file_num", file_num, "file index:", file_idx, "file_Size", file_size)

                # find first free spot
                free_idx = 0
                free_spots = 0
                found_free = False
                for i in range(0, total_size):
                    item = storage[i]
                    if not found_free and item == ".":
                        free_idx = i
                        found_free = True
                    if found_free:
                        if item == ".":
                            free_spots += 1
                        else:
                            break
                # print("next free idx", free_idx, "free_spots", free_spots)

            # print(storage)
            # print()
        count += 1
        # if count > 10:
        #     break

    # get answer
    total = 0
    for i in range(total_size):
        item = storage[i]
        if item != ".":
            total += i * storage[i]
    print(storage)
    print("TOTAL", total)

if __name__ == "__main__":
    # print("\nPART 1 RESULT")
    # start = time.perf_counter()
    # part1()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
