import sys, time, re, math

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    return None

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
sol1 = solve()
sol2 = solve()

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
