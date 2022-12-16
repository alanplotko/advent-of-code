import sys, time

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
data = sorted([sum(map(int, x.split(','))) for x in ((','.join([line.rstrip() for line in sys.stdin.readlines()])).split(',,'))],reverse=True)

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1 = data[0]
sol2 = sum(data[:3])

# Log execution time
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
