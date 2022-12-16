import sys, time

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
# Work in sliced chunks of the string, checking if the set matches the marker length to work with
def solve(data, markerLength):
    # Start position is first character (0) to last character that can fit the marker length
    for idx in range(0, len(data) - markerLength - 1):
        # If any character is deduped from set, then it's not all unique and < marker length
        if len(set([*data[idx:idx + markerLength]])) == markerLength:
            # We want the end position (start position + marker length)
            return idx + markerLength

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
# Parse stream as string
data = [line.rstrip() for line in sys.stdin.readlines()][0]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
# Get end position for string with marker length of 4 and 14
sol1 = solve(data, 4)
sol2 = solve(data, 14)

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
