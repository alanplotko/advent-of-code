import sys, time, re, math
from collections import deque

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# Array access for material costs in order of ascending value
ORE, CLAY, OBSIDIAN, GEODE = 0, 1, 2, 3

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve(costs, minutes=24, inventory=[0, 0, 0, 0], bots=[1, 0, 0, 0]):
    # Max number of bots for a given mineral type is bounded by the max cost for that mineral
    # for any bot. Any more would be diminishing returns, as we'd already be producing enough to make
    # 1 bot per minute. Maximum geode bots bounded to total minutes (m), i.e. in the best case where
    # geode bots cost nothing, we can still only spend m time to make m bots.
    maxBots = [max([cost[mineralType] for cost in costs]) for mineralType in range(3)] + [minutes]

    # Decision tree begins with time = 0, empty inventory, 1 ore bot, and no prior bot choices to work with
    decisions = deque([(0, inventory, bots, [])])

    # Track max geodes produced at a given time interval
    maxGeodes = {}

    if DEBUG:
        print(f"Max expense per mineral type: {maxBots}")

    # While decision tree has decisions to process, we keep going
    while decisions:
        time, inventory, bots, skipped = decisions.popleft()
        maxGeodes[time] = max(maxGeodes[time] if time in maxGeodes else 0, inventory[GEODE])
        # Proceed if we have enough time left and this branch is worth exploring further
        if time <= minutes and maxGeodes[time] == inventory[GEODE]:
            # Phase 1: What can we build?

            # Default (do nothing)
            botsToPurchase = [None]

            # Add any bot we have sufficient inventory to buy
            botsToPurchase.extend([bot for bot, cost in enumerate(costs) if all(x <= y for x, y in zip(cost, inventory))])

            # We must prioritize geode if possible to buy
            if GEODE in botsToPurchase:
                botsToPurchase = [GEODE]

            # Record each purchase as a decision to process in the decision tree
            for purchase in botsToPurchase:

                # A. We buy nothing
                if purchase == None:
                    # Update inventory with production this round
                    nextInventory = inventory.copy()
                    for i in range(4):
                        nextInventory[i] += bots[i]
                    # Track the bots we skipped this round for next round.
                    decisions.append((time + 1, nextInventory, bots, botsToPurchase))

                # B. We discard the puchase since we skipped it last round, or
                # we're at diminishing returns if we make the purchase
                elif purchase in skipped or bots[purchase] + 1 > maxBots[purchase]:
                    continue

                # C. We purchase the bot
                else:
                    # Update inventory with production this round. This does not include
                    # the bot that we buy, as it spends a minute to set up instead.
                    nextInventory = inventory.copy()
                    for i in range(4):
                        nextInventory[i] += bots[i]

                    # Pay cost from inventory accordingly
                    for idx, cost in enumerate(costs[purchase]):
                        nextInventory[idx] -= cost

                    # Track that we purchased the bot
                    nextBots = bots.copy()
                    nextBots[purchase] += 1

                    # Pass new inventory and bot states
                    decisions.append((time + 1, nextInventory, nextBots, []))

                    if TRACE:
                        print(f"{inventory} - {costs[purchase]} = {nextInventory}")
                        print(f"{bots} -> {nextBots}")

    return maxGeodes[minutes]

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
data = [list(map(int, re.findall(r'\d+', line))) for line in [line.rstrip() for line in sys.stdin.readlines()]]

# For each blueprint, we store the costs by element index mapping to mineral type (ORE, CLAY, OBSIDIAN, GEODE)
blueprints = []
for match in data:
    blueprints.append([(match[1], 0, 0, 0), (match[2], 0, 0, 0), (match[3], match[4], 0, 0), (match[5], 0, match[6], 0)])

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
# For solution 1, the elephants are hungry. We need the sum of blueprint quality = blueprint id (idx + 1) * max geodes obtainable in 24 minutes
mapping1 = {idx + 1: solve(blueprint) for idx, blueprint in enumerate(blueprints)}

# For solution 2, elephants ate our homework, but now they're not so hungry, so we have 32 minutes to work with just the first 3 blueprints.
# We need the product of max geodes obtainable in each remaining blueprint when working in 32 minutes.
mapping2 = [solve(blueprint, minutes=32) for blueprint in blueprints[:3]]

# Sum of each blueprint's quality
sol1 = sum([idx * maxGeodes for idx, maxGeodes in mapping1.items()])

# Product of each blueprint's max geodes obtainable
sol2 = math.prod(mapping2)

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
