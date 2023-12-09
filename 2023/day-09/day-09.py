import sys, time, re, math, functools

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    # Compute differences per sequence until we reach all zeroes
    mapping = {}
    for idx, seq in enumerate(data):
        mapping[idx] = [seq]
        done = False
        current = seq
        while not done:
            mapping[idx].append([current[n] - current[n-1] for n in range(1, len(current))])
            current = mapping[idx][-1]
            unique_numbers = list(set(current))
            if len(unique_numbers) == 1 and unique_numbers[0] == 0:
                done = True

    # Compute forward history
    fwd_hist_total = 0
    for _, seq in mapping.items():
        last = [level[-1] for level in seq[:len(seq) - 1]]
        fwd_hist_total += functools.reduce(lambda a, b: a + b, last)

    # Compute back history
    back_hist_total = 0
    for _, seq in mapping.items():
        first = [level[0] for level in reversed(seq[:len(seq) - 1])]
        back_hist_total += functools.reduce(lambda a, b: b - a, first)

    return fwd_hist_total, back_hist_total

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
data = [list(map(int, line.rstrip().split())) for line in sys.stdin.readlines()]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1, sol2 = solve()

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
