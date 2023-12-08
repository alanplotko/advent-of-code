import sys, time, re, math

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# For sol 1, compare full path
def compare_s1(current):
    return current != 'ZZZ'

# For sol 2, compare the last character
def compare_s2(current):
    return current[-1] != 'Z'

def compute_dist(current, mapping, comparator):
    steps = 0
    pointer = 0
    while comparator(current):
        current = mapping[current][0 if data[0][pointer % len(data[0])] == 'L' else 1]
        steps += 1
        pointer += 1
    return steps

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    mapping = {item.split(" = ")[0]: item.split(" = ")[1].replace('(','').replace(')','').split(", ") for item in data[1:]}

    # Sol 2: Precompute best distance per path looking at last character only
    sol2_distances = {item: compute_dist(item, mapping, compare_s2) for item in mapping.keys() if item[-1] == 'A'}

    # Sol 1: Compute distance from AAA to ZZZ
    # Sol 2: Compute LCM to find where all points end with Z
    return compute_dist('AAA', mapping, compare_s1), math.lcm(*sol2_distances.values())

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
