import sys, time
from collections import deque

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

# Parse data (flip x/y coordinates to align to row/col format instead)
data = [[tuple([int(x.split(',')[1]), int(x.split(',')[0])]) for x in line] for line in [x.split(' -> ') for x in [line.rstrip() for line in sys.stdin.readlines()]]]

# Read x and y coordinates to derive mins and maxes
cols = set([item[1] for data in data for item in data])
rows = set([item[0] for data in data for item in data])
minCol = min(cols)
maxCol = max(cols)
maxRow = max(rows)

# Shift column range to become 0-indexed instead, e.g. 494 -> 503 range becomes 0 -> 9
data = [[tuple([coord[0], coord[1] - minCol]) for coord in data] for data in data]

# Determine grid size
width = maxCol - minCol + 1
height = maxRow + 1

# Sand starts at fixed point in grid
sandStart = tuple([0, 500 - minCol])

if DEBUG:
    print(f"Min X = {minCol}, max X = {maxCol}, max Y = {maxRow}")
    print(f"{width} x {height} grid with sand start at {sandStart}")

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''

# Connect the lines per the given points
def computeFullPath(path):
    fullPath = set()
    for i in range(len(path) - 1):
        # Get current and adjacent coordinate
        a = path[i]
        b = path[i + 1]

        # Add starting point to path
        fullPath.add(a)

        # If row is the same, then connect by column
        if a[0] == b[0]:
            # Connect going left
            if a[1] > b[1]:
                for j in range(1, a[1] - b[1]):
                    fullPath.add(tuple([a[0], a[1] - j]))
            # Connect going right
            else:
                for j in range(1, b[1] - a[1]):
                    fullPath.add(tuple([a[0], a[1] + j]))
        # If col is the same, then connect by row
        else:
            # Connect going down
            if a[0] > b[0]:
                for j in range(1, a[0] - b[0]):
                    fullPath.add(tuple([a[0] - j, a[1]]))
            # Connect going up
            else:
                for j in range(1, b[0] - a[0]):
                    fullPath.add(tuple([a[0] + j, a[1]]))
        fullPath.add(b)

    if TRACE: print(fullPath)
    return fullPath

# Get next position for dropping sand
def getNextPosition(grid, sandStart, expand):
    row, col = sandStart[0], sandStart[1]
    sandRest = False

    if TRACE: print(f"START: {row}, {col}")

    while not sandRest:
        try:
            # DOWN
            if grid[row + 1][col] == '.':
                if TRACE: print(f"DOWN: {row + 1}, {col}")
                row += 1
            # DIAGONAL LEFT
            elif col - 1 >= 0 and grid[row + 1][col - 1] == '.':
                if TRACE: print(f"DIAGONAL LEFT: {row + 1}, {col - 1}")
                row += 1
                col -= 1
            # DIAGONAL RIGHT
            elif col + 1 < len(grid[0]) and grid[row + 1][col + 1] == '.':
                if TRACE: print(f"DIAGONAL RIGHT: {row + 1}, {col + 1}")
                row += 1
                col += 1
            # Check bounds, especially if expansion is enabled
            elif col - 1 < 0:
                if TRACE: print(f"Out of scope at {row + 1}, {col - 1}")

                if not expand:
                    return [None, sandStart]

                if TRACE: print(f"Expanding on left by 3 for col {col}")

                for idx, x in enumerate(grid):
                    if idx == len(grid) - 1:
                        grid[idx].extendleft(['#' for x in range(3)])
                    else:
                        grid[idx].extendleft(['.' for x in range(3)])

                sandStart = tuple([sandStart[0], sandStart[1] + 3])
                row, col = sandStart[0], sandStart[1]
                if TRACE: print(f"Retrying at START = {row}, {col}")

            # Check bounds, especially if expansion is enabled
            elif col >= len(grid[0]) - 1:
                if TRACE: print(f"Out of scope at {row + 1}, {col + 1}")

                if not expand:
                    return [None, sandStart]

                if TRACE: print(f"Expanding on right by 3 for col {col}")

                for idx, x in enumerate(grid):
                    if idx == len(grid) - 1:
                        grid[idx].extend(['#' for x in range(3)])
                    else:
                        grid[idx].extend(['.' for x in range(3)])

                row, col = sandStart[0], sandStart[1]
                if TRACE: print(f"Retrying at START = {row}, {col}")

            else:
                sandRest = True

        # Check bounds, cover remaining edge cases
        except IndexError as e:
            sandRest = True
            if TRACE: print(f"Out of scope at {row}, {col}")
            return [None, sandStart]

    # Drop sand at coord in grid
    grid[row][col] = 'o'
    if TRACE:
        print(f"Adding sand to {row}, {col}")
        for line in grid:
             print(''.join(line))

    return [tuple([row, col]), sandStart]

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''

def solve(data, sandStart, expand, filenamePrefix):
    # Grid height gets +2 for solution 2 due to infinite width floor at max Y + 2
    grid = [deque(['.' for x in range(width)]) for y in range(height + 2 if expand else height)]
    sandRow, sandCol = sandStart
    grid[sandRow][sandCol] = '+'

    # Set up infinite floor for solution 2
    if expand:
        lastRow = len(grid) - 1
        for col in range(width):
            grid[lastRow][col] = '#'
    # Connect the lines
    for path in data:
        fullPath = computeFullPath(path)
        for row, col in fullPath:
            grid[row][col] = '#'

    # Count sand dropped
    sandOutOfScope = False
    sandCount = 0
    while not sandOutOfScope:
        result = getNextPosition(grid, sandStart, expand)
        position, sandStart = result
        # If no position returned, or if position = start point for dropping sand, then we're done
        if position == None or position == sandStart:
            sandOutOfScope = True
            if expand:
                sandCount += 1 # Include the last drop of sand at the start point
        else:
            sandCount += 1

    # Write final grid output to file for visualization
    f = open(filenamePrefix + "-output.txt", "w")
    for line in grid:
        f.write(''.join(line) + "\n")
    f.close()

    return sandCount

'''''''''''''''''''''
LOG SOLUTIONS
'''''''''''''''''''''

sol1 = solve(data, sandStart, False, 'sol1')
sol2 = solve(data, sandStart, True, 'sol2')

print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")

# Log execution time
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
