import sys, time

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
def is_valid(data):
    decreasing = [data[i] > data[i + 1] and 1 <= data[i] - data[i + 1] <= 3 for i in range(len(data) - 1)]
    increasing = [data[i] < data[i + 1] and 1 <= data[i + 1] - data[i] <= 3 for i in range(len(data) - 1)]
    return all(decreasing) or all(increasing)

def is_valid_with_one_level_removed(data):
    for i in range(len(data)):
        data_level_removed = data[:i] + data[i + 1:]
        if is_valid(data_level_removed):
            return True
    return False

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve1(lists):
    return sum(is_valid(data) for data in lists)

def solve2(lists):
    return sum(is_valid(data) or is_valid_with_one_level_removed(data) for data in lists)

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
