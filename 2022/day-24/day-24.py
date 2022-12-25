import sys, time
from collections import deque
from operator import add

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# Denote ground as '.' and use arrows.keys() for parsing blizzards
GROUND = '.'
arrows = {'>': (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0)}

# Can stay in same position or move 1 right, down, left, or up
movementDeltas = set([(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)])

# Get next positions taking into account grid bounds and blizzard locations blocking the way
def getNextPositions(position, blocked, minutes):
    return [(minutes, (row, col)) for row, col in [tuple(map(add, position, delta)) for delta in movementDeltas]
        if (row, col) not in blocked and ((row, col) == start or (row, col) == end or (row >= 0 and row < totalRows and col >= 0 and col < totalCols))
    ]

# Get the state of blizzards after m minutes, which we may have captured previously and can reuse.
# Return the map keys (blizzard locations) as we don't need the directional information outside of
# computing blizzard locations.
def getBlizzardLocationsAtTime(minutes):
    if minutes in blizzardsMemoMap:
        return blizzardsMemoMap[minutes].keys()

    blizzardsAtTime = {}
    for location, directions in blizzards.items():
        row, col = location
        newLocations = [((
            ((arrows[direction][0] * minutes) + row) % totalRows,
            ((arrows[direction][1] * minutes) + col) % totalCols
        ), direction) for direction in directions]
        for pair in newLocations:
            newLocation, direction = pair
            if newLocation in blizzardsAtTime:
                blizzardsAtTime[newLocation].append(direction)
            else:
                blizzardsAtTime[newLocation] = [direction]
    blizzardsMemoMap[minutes] = blizzardsAtTime
    return blizzardsAtTime.keys()

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
# Given initial start and end coords, make l laps back and forth between the points
def solve(start, end, laps):
    # Count decision evaluations for stats
    evaluated = 0

    # Track visited points by time
    visited = set()

    # Track each lap, sol 1 needs the first lap time and sol2 needs the last lap time
    lapTimes = []
    decisions = deque([(0, start)])

    for i in range(laps):
        while decisions:
            minutes, position = decisions.popleft()
            evaluated += 1

            if TRACE:
                print(f"Decisions evaluated = {evaluated} vs remaining = {len(decisions)}, time = {minutes}", end='\r')

            # When we arrive at the end coord, then we can track the time taken and swap start and end to make our way back
            if position == end:
                if DEBUG or TRACE:
                    print(f"Decisions evaluated = {evaluated} vs remaining = {len(decisions)}, time = {minutes}, blizzard maps = {len(blizzardsMemoMap)}")

                # Track time taken
                lapTimes.append(minutes)

                # Swap start and end
                tmp = start
                start = end
                end = tmp

                # Clear decision deque and add new starting point
                decisions.clear()
                decisions.append([minutes, start])
                break

            # Don't continue down paths we've already visited at the same time
            if (minutes, position) not in visited:
                visited.add((minutes, position))
                blocked = getBlizzardLocationsAtTime(minutes + 1)
                options = getNextPositions(position, blocked, minutes + 1)
                decisions.extend(options)

    return lapTimes

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
data = [[*line] for line in [line.rstrip() for line in sys.stdin.readlines()]]

# Determine start and end coords after removing walls (#) from input
'''
S
>>.<^<
.<..<<
>v.><>
<^v^^>
     E
'''
totalRows, totalCols = len(data) - 2, len(data[0]) - 2

# Start from above inner grid (row = -1) and account for wall removal
start = (-1, data[0].index(GROUND) - 1)

# End below inner grid and account for wall removal
end = (totalRows, data[-1].index(GROUND) - 1)

if DEBUG:
    print(f"Start = {start}, end = {end}, total rows = {totalRows}, total cols = {totalCols}")

# Set up blizzard locations as dicts
blizzards = {}
blizzardUid = 0

# Navigate inner grid
for row in range(1, totalRows + 1):
    for col in range(1, totalCols + 1):
        key = data[row][col]
        # Only capture arrows indicating initial blizzard positions in grid
        if key in arrows.keys():
            # Subtract 1 from row and col to account for wall removal
            position = (row - 1, col - 1)
            if position in blizzards:
                blizzards[position].append(key)
            else:
                blizzards[position] = [key]

# Track blizzard positions by time, 0 = initial positions
blizzardsMemoMap = {0: blizzards}

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
# Sol 1 = time spent going from start -> end for total minutes at lap 1
# Sol 2 = time spent going from start -> end -> start -> end for total minutes at lap 3
# Ignore the time at lap 2 on the way back to grab the snacks we forgot for the elves
sol1, _, sol2 = solve(start, end, 3)

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
