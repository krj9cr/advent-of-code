import time

class Card:
    def __init__(self, id, winning, mine):
        self.id = id
        self.winning = winning
        self.mine = mine

    def __str__(self):
        return str(self.id) + "; " + str(self.winning) + "; " + str(self.mine)

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        # lines = [line.strip() for line in file]
        cards = []
        for line in file:
            line = line.strip()
            parts1 = line.split(": ")
            # print(parts1)
            cardId = int(parts1[0].strip("Card "))
            parts2 = parts1[1].split(" | ")
            # print(parts2)
            winning = [int(num) for num in parts2[0].strip().replace("  ", " ").split(" ")]
            mine = [int(num) for num in parts2[1].strip().replace("  ", " ").split(" ")]
            cards.append(Card(cardId, winning, mine))
        return cards

def part1():
    cards = parseInput(4)
    answer = 0
    for card in cards:
        point = 1
        total_points = 0
        first_match = True
        print(card)
        for m in card.mine:
            if m in card.winning:
                if first_match:
                    total_points = 1
                    first_match = False
                else:
                    total_points *= 2
        print(total_points)
        answer += total_points
    print(answer)

card_always_copied = {}

def process_card(card, cards):
    num_winning = 0
    card_copies = []
    for m in card.mine:
        if m in card.winning:
            num_winning += 1
    # print(num_winning)
    for i in range(0, num_winning):
        card_copies.append(i + card.id + 1)
        copy_copies = process_card(cards[i + card.id], cards)
        if len(copy_copies) > 0:
            card_copies += copy_copies
    card_always_copied[card.id] = card_copies
    print(card.id, card_copies)
    return card_copies

def part2():
    cards = parseInput(4)
    answer = 0
    card_totals = {}
    for card in cards:
        print(card)
        if card_totals.get(card.id):
            card_totals[card.id] += 1
        else:
            card_totals[card.id] = 1

        cards_copied = []
        if card_always_copied.get(card.id):
            cards_copied = card_always_copied[card.id]
        else:
            cards_copied = process_card(card, cards)
        for cardId2 in cards_copied:
            if card_totals.get(cardId2):
                card_totals[cardId2] += 1
            else:
                card_totals[cardId2] = 1

    for cardId in card_totals:
        answer += card_totals[cardId]

    print(card_totals)
    print(answer)

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
