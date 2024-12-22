import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append(int(line))
        return lines

def part1():
    secrets = parseInput(22)
    print(secrets)

    total = 0
    for secret in secrets:
        print(secret)
        for i in range(10):
            one = secret * 64
            newSecret = secret ^ one
            newSecret = newSecret % 16777216
            two = newSecret // 32
            newSecret = newSecret ^ two
            newSecret = newSecret % 16777216
            three = newSecret * 2048
            newSecret = newSecret ^ three
            newSecret = newSecret % 16777216
            secret = newSecret
            print(secret)
        total += secret
        print()
    print("Total", total)

def part2():
    secrets = parseInput(22)
    print(secrets)

    secret_prices = {}
    for secret in secrets:
        print(secret)
        # get price
        price = abs(secret) % 10
        # print(secret, ":", price)
        secret_prices[secret] = [price]
        og_secret = secret
        for i in range(2000):
            one = secret * 64
            newSecret = secret ^ one
            newSecret = newSecret % 16777216
            two = newSecret // 32
            newSecret = newSecret ^ two
            newSecret = newSecret % 16777216
            three = newSecret * 2048
            newSecret = newSecret ^ three
            newSecret = newSecret % 16777216
            secret = newSecret
            # get ones digit
            price = abs(secret) % 10
            # print(secret, ":", price)
            secret_prices[og_secret].append(price)
        # print()
    print(secret_prices)

    # get the diffs...?
    secret_diffs = {}
    for secret in secret_prices:
        prices = secret_prices[secret]
        diffs = []
        for i in range(len(prices)-1):
            p1 = prices[i]
            p2 = prices[i+1]
            diff = p2 - p1
            diffs.append(diff)
        secret_diffs[secret] = diffs
    print(secret_diffs)

    # do a sliding window of size 4 over the first sequence
    first_secret = secrets[0]
    first_diffs = secret_diffs[first_secret]
    first_prices = secret_prices[first_secret]

    window_size = 4
    max_cost = 0
    for i in range(len(first_diffs) - window_size + 1):
        first_changes = first_diffs[i: i + window_size]

        # first, just make sure we got the right number
        # if first_changes == [-2, 1, -1, 3]:
        first_cost = first_prices[i+window_size]
        total_cost = first_cost
        # print(first_changes, first_cost)

        # try finding the first value in other secret_diffs where that sequence occurs, it could not occur, too
        for s in range(1, len(secrets)):
            secret = secrets[s]
            diffs = secret_diffs[secret]
            prices = secret_prices[secret]

            for j in range(len(diffs) - window_size + 1):
                changes = diffs[j: j + window_size]
                if changes == first_changes:
                    cost = prices[j + window_size]
                    total_cost += cost
                    # print("SAME", secret, cost)
        if total_cost > max_cost:
            max_cost = total_cost
            print("best cost", total_cost, first_changes)

    # sum everything
    # find the max

# 1881 too low

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
