import sys, time, math

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
def compute_ways_to_win(data):
    wins = [0] * len(data[0])
    for i in range(0, len(data[0])):
        dist = data[0][i]
        record = data[1][i]
        for j in range(1, dist):
            if j * (dist - j) > record:
                wins[i] += 1
    return math.prod(wins)

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    kerned_data = [[int(''.join(map(str, d)))] for d in data]
    return compute_ways_to_win(data), compute_ways_to_win(kerned_data)

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
data = [list(map(int, line.split(': ')[1].split())) for line in sys.stdin.readlines()]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1, sol2 = solve()

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
