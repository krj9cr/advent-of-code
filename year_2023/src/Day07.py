import time

cardValues = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2
}

handKinds = {
    "five": 7,
    "four": 6,
    "fullhouse": 5,
    "three": 4,
    "two pair": 3,
    "one pair": 2,
    "high": 1
}

class HandBid:
    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid
        self.cardCounts = self.countCards()
        self.handKind = self.detectHandKind()

    def __str__(self):
        return str(self.hand) + " " + str(self.bid)

    def countCards(self):
        cardCounts = {}
        for card in self.hand:
            if cardCounts.get(card):
                cardCounts[card] += 1
            else:
                cardCounts[card] = 1
        return cardCounts

    # return 1-7 based on hand kind
    def detectHandKind(self):
        numUniqueCards = len(self.cardCounts)
        if numUniqueCards == 1:  # five of a kind
            return 7
        if numUniqueCards == 2:  # four of a kind or full house
            for card in self.cardCounts:
                count = self.cardCounts[card]
                if count == 4:
                    return 6  # four of a kind
                if count == 2 or count == 3:
                    return 5  # full house
                if count == 1:
                    return 6  # four of a kind
        if numUniqueCards == 3:  # three of a kind or two pair
            maxCount = 0
            for card in self.cardCounts:
                count = self.cardCounts[card]
                if count > maxCount:
                    maxCount = count
            if maxCount == 3:  # three of a kind
                return 4
            else:
                return 3  # two pair
        if numUniqueCards == 4:  # one pair
            return 2
        if numUniqueCards == 5:  # high card
            return 1

    def __lt__(self, other):
        hand1 = self.hand
        hand2 = other.hand

        # sort by hand type
        if self.handKind == other.handKind:
            for i in range(0, len(self.hand)):
                card1 = self.hand[i]
                card2 = other.hand[i]
                if cardValues[card1] == cardValues[card2]:
                    continue
                else:
                    return cardValues[card1] < cardValues[card2]
        return self.handKind < other.handKind

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        handBids = []
        for line in file:
            l = line.strip().split(" ")
            hand = l[0]
            bid = int(l[1])
            handBids.append(HandBid(hand, bid))

        return handBids

def part1():
    handBids = parseInput(7)
    for handBid in handBids:
        print(handBid)
        print(handBid.detectHandKind())
        print()
    handBids.sort()
    answer = 0
    for i in range(0, len(handBids)):
        handBid = handBids[i]
        print(handBid)
        answer += handBid.bid * (i + 1)
    print(answer)

def part2():
    lines = parseInput(7)
    print(lines)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    # print("\nPART 2 RESULT")
    # start = time.perf_counter()
    # part2()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)
