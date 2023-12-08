import sys, time, re, math

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# Full path
def compare_s1(current):
    return current != 'ZZZ'

# Just the third character
def compare_s2(current):
    return current[2] != 'Z'

# For sol 1
def compute_dist_s1(current, mapping):
    steps = 0
    pointer = 0
    while compare_s1(current):
        current = mapping[current][0 if data[0][pointer % len(data[0])] == 'L' else 1]
        steps += 1
        pointer += 1
    return steps

# For sol 2
def compute_dist_s2(current, mapping):
    steps = 0
    pointer = 0
    while compare_s2(current):
        current = mapping[current][0 if data[0][pointer % len(data[0])] == 'L' else 1]
        steps += 1
        pointer += 1
    return steps

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    mapping = {item.split(" = ")[0]: item.split(" = ")[1].replace('(','').replace(')','').split(", ") for item in data[1:]}

    # Sol 1: Compute distance from AAA to ZZZ
    dist = compute_dist_s1('AAA', mapping)

    # Sol 2: Precompute best distance per path looking at last character only
    current = {item: 0 for item in mapping.keys() if item[-1] == 'A'}
    for item in current:
        current[item] = compute_dist_s2(item, mapping)

    # Compute LCM to find where all points end with Z
    lcm = math.lcm(*current.values())

    return dist, lcm

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
data = [line.rstrip() for line in sys.stdin.readlines() if line.rstrip() != '']

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1, sol2 = solve()

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
