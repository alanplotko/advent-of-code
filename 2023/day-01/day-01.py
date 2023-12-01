import sys, time, regex

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve(pattern, useMapping = False):
    mapping = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}
    sol = 0
    for line in data:
        firstMatch = regex.search(pattern, line)
        lastMatch = regex.search('(?r)' + pattern, line)
        first = firstMatch.group() if firstMatch != None and firstMatch.group().isdigit() else mapping[firstMatch.group()]
        last = lastMatch.group() if lastMatch != None and lastMatch.group().isdigit() else mapping[lastMatch.group()]
        sol += int(first + last)
    return sol

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
sol1 = solve("\d")
sol2 = solve("(\d|one|two|three|four|five|six|seven|eight|nine)", True)

# Log execution time
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
