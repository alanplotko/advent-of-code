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
data = [x.split() for x in [line.rstrip() for line in sys.stdin.readlines()]]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
# Part 1
# Components: list of [shape score, result score].
# Shape score: Map X-Z to 1-3.
# Result score: Map A-C and X-Z to 0-2, your move - their move = 0 if
#   same move (draw) and either 1 or -2 if your win. You can modulo 3 to
#   consolidate to only 1 on win. Then map to result points (0, 3, 6)
#   and sum them up.
components = [[ord(x[1]) - 87, ((ord(x[1]) - 88) - (ord(x[0]) - 65)) % 3] for x in data]
sol1 = sum([x[0] + (3 if x[1] == 0 else (6 if x[1] == 1 else 0)) for x in components])

# Part 2
# Shape score: requires computing the shape you play.
#   You know the result from X-Z, where X = lose, Y = draw, Z = win. If we go
#   by the 0-2 mapping, you need to be down by 1, same value, or up by 1
#   for # -1, 0, 1. We can use ord(x[1]) - 89) to get the -1, 0, 1 to add to
#   the A-C's mapped value, modulo 3 to keep in the required 0-2 range, and
#   add 1 because the shape score is 1-3.
# Result score: we can nap X-Z to 0-2 where X/0 = lose, Y/1 = draw, Z/2 = win.
#   Fortunately, the result points are 0, 3, and 6 respectively, which we
#   can transform to by 0-2 * 3 = (0, 3, 6), and sum them up.
sol2 = sum([((((ord(x[0]) - 65) + (ord(x[1]) - 89)) % 3) + 1) + ((ord(x[1]) - 88) * 3) for x in data])

# Log execution time
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
