import sys, time

'''''''''''''''''''''
SETUP
'''''''''''''''''''''

# Start timer
startTime = time.time()

# Print statements
DEBUG = False
TRACE = False

'''''''''''''''''''''
DATA PARSING
'''''''''''''''''''''

# Parse data
data = [line.rstrip() for line in sys.stdin.readlines()]

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''



'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''

def solve():
    return None

'''''''''''''''''''''
LOG SOLUTIONS
'''''''''''''''''''''

sol1 = solve()
sol2 = solve()

print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")

# Log execution time
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
