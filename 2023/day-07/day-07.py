import sys, time, re, math, functools

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
FIVE_KIND = 7
FOUR_KIND = 6
FULL_HOUSE = 5
THREE_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

def compute_rank(hand):
    # Operate with Jokers if 'J' is smallest individual rank
    if RANKS[0] == 'J':
        mapping = sorted(({card: hand.count(card) for card in set(hand) if card != 'J'}).items(), key=lambda x:x[1], reverse=True)
        jokers = hand.count('J')
    else:
        mapping = sorted(({card: hand.count(card) for card in set(hand)}).items(), key=lambda x:x[1], reverse=True)
        jokers = 0

    # If all jokers, then they would choose the strongest five of a kind
    if jokers == 5:
        mapping = [('A', 5)]
    # Otherwise, if any jokers, pick the most common card to add to
    elif jokers > 0:
        lst = list(mapping[0])
        lst[1] += jokers
        mapping[0] = tuple(lst)

    # Compute score
    card, count = mapping[0]
    if count == 5:
        return FIVE_KIND
    elif count == 4:
        return FOUR_KIND
    elif count == 3:
        card, count = mapping[1]
        if count == 2:
            return FULL_HOUSE
        return THREE_KIND
    elif count == 2:
        card, count = mapping[1]
        if count == 2:
            return TWO_PAIR
        return ONE_PAIR

    return HIGH_CARD

def compare_hands(hand1, hand2):
    hand1 = hand1[0]
    hand2 = hand2[0]
    score1 = compute_rank(hand1)
    score2 = compute_rank(hand2)
    if score1 < score2:
        return -1
    elif score1 > score2:
        return 1
    else:
        for i in range(len(hand1)):
            if RANKS.index(hand1[i]) < RANKS.index(hand2[i]):
                return -1
            elif RANKS.index(hand1[i]) > RANKS.index(hand2[i]):
                return 1
        return 0

def compute_winnings():
    data.sort(key=functools.cmp_to_key(compare_hands))
    return sum([hand[1] * (idx + 1) for idx, hand in enumerate(data)])

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    # We need to edit the global ranks when we get to sol 2
    global RANKS

    # Compute winnings for sol 1
    winnings_sol1 = compute_winnings()

    # Compute winnings with rank change for sol 2
    RANKS.insert(0, RANKS.pop(RANKS.index('J')))
    winnings_sol2 = compute_winnings()

    return winnings_sol1, winnings_sol2

'''''''''''''''''''''
SETUP
'''''''''''''''''''''
# Print statements
DEBUG = False
TRACE = False

# Start timer
startTime = time.time()

'''''''''''''''''''''
DATA PARSING
'''''''''''''''''''''
# Parse data
data = [[line.rstrip().split(' ')[0], int(line.rstrip().split(' ')[1])] for line in sys.stdin.readlines()]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1, sol2 = solve()

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
