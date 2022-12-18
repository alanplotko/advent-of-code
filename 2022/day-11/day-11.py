import sys, time, math
from collections import deque
from copy import deepcopy

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve(monkeys, rounds, worryDivisor, commonMod):
    for i in range(rounds):
        if DEBUG:
            print("Round %d" % (i + 1), flush=True)

        for monkey in monkeys:
            while monkey['items']:
                monkey['inspectCount'] += 1
                newWorryLevel = monkey['operation'](monkey['items'].popleft())
                if worryDivisor != None:
                    newWorryLevel //= worryDivisor
                elif commonMod != None:
                    newWorryLevel %= commonMod
                result = newWorryLevel % monkey['divisibleBy'] == 0
                # Get monkey index to pass to based on divisibility test result
                monkeys[monkey['test'](result)]['items'].append(newWorryLevel)

            if DEBUG:
                print([monkey['items'] for monkey in monkeys])
                print("Monkey %d throws old %d to monkey %d as %d" % (monkey['id'], old, monkey[str(result)], newWorryLevel))
    inspectCounts = [monkey['inspectCount'] for monkey in monkeys]
    return math.prod(sorted(inspectCounts)[-2:])

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
data = [line.strip() for line in sys.stdin.readlines() if line.strip() != '']

# Parse monkeys as objects in list
monkeys = []
for i in range(0, len(data), 6):
    chunk = data[i:i+6]
    # Makes eval faster?
    expression = chunk[2].split("Operation: new = ")[1]
    evalFunc = eval('lambda old: ' + expression)
    testFunc = eval('lambda x: %d if x else %d' % (
        int(chunk[4].split("If true: throw to monkey ")[1]),
        int(chunk[5].split("If false: throw to monkey ")[1])
    ))
    monkeys.append({
        'id': int(chunk[0][:-1].split()[1]),
        'items': deque([int(x) for x in chunk[1].replace(",", "").split("Starting items: ")[1].split()]),
        'divisibleBy': int(chunk[3].split("Test: divisible by ")[1]),
        'operation': evalFunc,
        'test': testFunc,
        'inspectCount': 0
    })

commonMod = math.prod([monkey['divisibleBy'] for monkey in monkeys])

if DEBUG:
    for monkey in monkeys:
        print(monkey)

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1 = solve(deepcopy(monkeys), 20, 3, None)
sol2 = solve(deepcopy(monkeys), 10000, None, commonMod)

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
