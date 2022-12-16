import sys, time

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
def getPriority(letter):
    return ord(letter) - 38 if letter.isupper() else ord(letter) - 96

def findCommon(arr):
    return ''.join(set.intersection(*map(set, arr)))

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
data = [line.rstrip() for line in sys.stdin.readlines()]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
part1 = [[x[:len(x)//2], x[len(x)//2:]] for x in data]
part2 = [x for x in (data[i:i + 3] for i in range(0, len(data), 3))]

sol1 = sum(list(map(getPriority, [findCommon(x) for x in part1])))
sol2 = sum(list(map(getPriority, [findCommon(x) for x in part2])))

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
