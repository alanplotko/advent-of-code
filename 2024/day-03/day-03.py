import sys, time, re

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve1(data):
    # Sum of products of all mul instructions parsed from input
    return sum([int(x) * int(y) for x, y in re.findall(r'mul\((\d+),(\d+)\)', data)])

def solve2(data):
    # Remove all instances of don't() -> do() before reusing solve1 for just the enabled mul instructions
    return solve1(re.sub(r"don\'t\(\).*?do\(\)", "", data))

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
data = ''.join([line.rstrip() for line in sys.stdin.readlines()])

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1 = solve1(data)
sol2 = solve2(data)

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
