import sys, time, re, math

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
def parse_cards(cards):
    winners, numbers = cards
    winners = list(map(int, winners.split()))
    numbers = list(map(int, numbers.split()))
    matches = len([w for w in winners if w in numbers])
    return {'winners': winners, 'numbers': numbers, 'matches': matches, 'copies': 1}


'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    # Split cards into winners and numbers and precompute matches (for sol 1)
    # and track copies (for sol 2)
    cards = [parse_cards(cards) for card_num, cards in enumerate(data)]

    # Sol 1: Calculate total score from matches per card
    total_score = sum([math.floor(2 ** (card['matches'] - 1)) for card in cards])

    # Sol 2: Update copies per card based on matches and track all cards scored
    total_cards = 0
    for card_num, entry in enumerate(cards):
        for i in range(card_num + 1, card_num + entry['matches'] + 1):
            cards[i]['copies'] += entry['copies']
        total_cards += entry['copies']

    return total_score, total_cards

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
data = [re.split('Card\s+\d+:\s+', line)[1].strip().split(' | ') for line in sys.stdin.readlines()]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1, sol2 = solve()

# # Log execution time
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
