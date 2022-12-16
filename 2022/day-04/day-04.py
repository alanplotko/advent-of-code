import sys, time

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
def exactRange(x):
    r1 = range(x[0], x[1] + 1)
    r2 = range(x[2], x[3] + 1)
    return 1 if set(r1).issubset(r2) or set(r2).issubset(r1) else 0

def partialRange(x):
    r1 = range(x[0], x[1] + 1)
    r2 = range(x[2], x[3] + 1)
    return 1 if x[0] in r2 or x[1] in r2 or x[2] in r1 or x[3] in r1 else 0

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
data = [list(map(int, x)) for x in [x.split(',') for x in [x.replace('-', ',') for x in [line.rstrip() for line in sys.stdin.readlines()]]]]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1 = sum(list(map(exactRange, data)))
sol2 = sum(list(map(partialRange, data)))

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
