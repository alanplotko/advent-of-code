import sys, time
from collections import Counter

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve1(data):
    list1, list2 = [sorted(list(x)) for x in zip(*data)]
    return sum([abs(list1[i] - list2[i]) for i in range(0, len(list1))])

def solve2(data):
    list1, list2 = [list(x) for x in zip(*data)]
    counts = Counter(list2)
    return sum([i * counts[i] for i in list1])

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
data = [[int(x) for x in line.rstrip().split()] for line in sys.stdin.readlines()]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1 = solve1(data)
sol2 = solve2(data)

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
