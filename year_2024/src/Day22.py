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

    NUM_ROUNDS = 2000

    secret_prices = {}
    for secret in secrets:
        print(secret)
        # get price
        price = abs(secret) % 10
        # print(secret, ":", price)
        secret_prices[secret] = [price]
        og_secret = secret
        for i in range(NUM_ROUNDS):
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

    windows = {}  # [1,2,3,4] => [cost, ...]
    secrets_seen_windows = {}  # secret_idx => set(seen_windows)

    for s in range(len(secrets)):
        secrets_seen_windows[s] = set()

    window_size = 4
    for s in range(len(secrets)):
        secret = secrets[s]
        for i in range(NUM_ROUNDS - window_size + 1):
            diffs = secret_diffs[secret]
            prices = secret_prices[secret]
            window = diffs[i: i + window_size]
            window_str = ','.join([str(num) for num in window])

            if window_str in secrets_seen_windows[s]:
                continue
            secrets_seen_windows[s].add(window_str)

            cost = prices[i+window_size]
            if windows.get(window_str) is not None:
                windows[window_str].append(cost)
            else:
                windows[window_str] = [cost]

    max_cost = 0
    best_window = None
    for window in windows:
        cost = sum(windows[window])
        if cost > max_cost:
            max_cost = cost
            best_window = window
    print(best_window, max_cost)

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
