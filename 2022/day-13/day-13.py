import sys, time, math
from functools import cmp_to_key

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# Recursive check function that takes left, right, and index for list where applicable
# 0 = equal
# -1 = less than (correct order)
# 1 = greater than (wrong order)
def check(left, right, idx = 0):
    # Both lists
    if isinstance(left, list) and isinstance(right, list):
        # If index in bounds for both, check item therein recursively
        if len(left) > idx and len(right) > idx:
            result = check(left[idx], right[idx])
            # If equal, then continue to check through list
            if result == 0:
                return check(left, right, idx + 1)
            # Return if we have a concrete result
            return result
        # If left list ends early, then left < right and in right order
        elif len(left) <= idx and len(right) > idx:
            return -1
        # If right list ends early, then left > right and in wrong order
        elif len(left) > idx and len(right) <= idx:
            return 1
        # If both lists out of bounds, then they're still equal since we continue
        # comparing while equal until order is confirmed right or wrong
        else:
            return 0
    # Both ints
    elif isinstance(left, int) and isinstance(right, int):
        # Less than = correct order
        if left < right:
            return -1
        # Greater than = wrong order
        elif left > right:
            return 1
        # Equal
        else:
            return 0
    # Mixed, convert int to list of int
    else:
        if isinstance(left, int):
            return check([left], right)
        else:
            return check(left, [right])

# Comparator for all pairs at once for solution 2
def compare(left, right):
    return check(left, right, 0)

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve(dividers):
    # Walk through pairs for solution 1
    results = []
    for i in range(0, len(pairs), 2):
        left = pairs[i]
        right = pairs[i + 1]
        result = check(left, right, 0)
        results.append(result)
        if DEBUG:
            print("Pair %d = %s\nLeft = %s ; Right = %s\n" % (len(results), result, left, right))

    pairs.extend(dividers)
    correctOrder = sorted(pairs, key=cmp_to_key(compare))
    return (results, correctOrder)

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
# Parse data as pairs
data = [line.rstrip() for line in sys.stdin.readlines()]
pairs = [eval(line) for line in data if line != '']

# Add dividers to pairs for solution 2
dividers = [[[2]], [[6]]]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
results, correctOrder = solve(dividers)

# Solution 1: Sum of pair #s (1-indexed) where order is right (result = -1)
sol1 = sum([idx + 1 if x == -1 else 0 for idx, x in enumerate(results)])

# Solution 2: Product of divider indices (1-indexed) after all packets (lines irrespective of initial pairs) are sorted
sol2 = math.prod([correctOrder.index(divider) + 1 for divider in dividers])

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
