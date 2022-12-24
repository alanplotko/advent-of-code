import sys, time, re

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# Track out of bounds (void), paths, and walls
VOID, PATH, WALL = ' ', '.', '#'

# Track directions in provided order
RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3
arrows = {0: '>', 1: 'v', 2: '<', 3: '^'}

# Print grid for visualization purposes. Useful for debugging.
def printGrid(grid):
    for row in grid:
        print(f"{''.join(row)}")

# Get next position to determine if movement is possible, i.e. you
# can't move out of bounds or through walls
def getNextPosition(grid, row, col, facing, cubeConfig):
    # Parse cube config if working in sol 2
    isCube, cubeEdgeMappings = cubeConfig

    # For sol 2, we wrap around from the current face to the new face
    if isCube:
        currentPosition = (row, col, facing)
        if currentPosition in cubeEdgeMappings:
            if DEBUG:
                print(f"Moved from {currentPosition} to {cubeEdgeMappings[(row, col, facing)]}")
            row, col, facing = cubeEdgeMappings[(row, col, facing)]
        else:
            if facing == LEFT and col - 1 >= 0:
                col -= 1
            elif facing == RIGHT and col + 1 < len(grid[0]):
                col += 1
            elif facing == UP and row - 1 >= 0:
                row -= 1
            elif facing == DOWN and row + 1 < len(grid):
                row += 1
    # For sol 1, we simply wrap around the row or col
    else:
        if facing == LEFT:
            col = (col - 1) % len(grid[row])
        elif facing == RIGHT:
            col = (col + 1) % len(grid[row])
        elif facing == UP:
            row = (row - 1) % len(grid)
        else:
            row = (row + 1) % len(grid)

        # For sol 1, if we ended up out of bounds, then we keep going until back in bounds
        if grid[row][col] == VOID:
            return getNextPosition(grid, row, col, facing, cubeConfig)

    # For both sols, if we hit a wall, indicate so, or return the new row, col, and direction facing
    if grid[row][col] == WALL:
        return WALL
    else:
        return (row, col, facing)

# Perform movement on the grid
def move(grid, row, col, movement, facing, cubeConfig):
    direction, steps = movement

    # Get new direction facing per the provided order
    facing = (facing + (1 if direction == 'R' else -1)) % len(arrows)
    grid[row][col] = arrows[facing]

    # Get next
    for i in range(steps):
        position = getNextPosition(grid, row, col, facing, cubeConfig)
        # Stop if we hit a wall
        if position == WALL:
            break
        # Parse new location and direction facing
        else:
            row, col, facing = position
            grid[row][col] = arrows[facing]
    return (row, col, facing)

# Set up edge mappings to navigate the cube in sol 2
def setUpCubeMappings():
    '''
    Cube mapping will follow this order
        |------|
        | 2  1 |
    |---| 3 |--|
    | 5   4 |
    | 6 |---|
    |---|
    '''
    cubeEdgeMappings = {}

    # Face 2 top (L->R) <-> face 6 left (U -> D)
    # Direction: U -> R or L -> D
    for i in range(50, 100):
        assert(data[0][i] != VOID)
        assert(data[i + 100][0] != VOID)
        cubeEdgeMappings[(0, i, UP)] = (i + 100, 0, RIGHT)
        cubeEdgeMappings[(i + 100, 0, LEFT)] = (0, i, DOWN)

    # Face 1 top (L->R) <-> face 6 bottom (L->R)
    # Direction stays consistent, U -> U or D -> D
    for i in range(100, 150):
        assert(data[0][i] != VOID)
        assert(data[totalRows - 1][i - 100] != VOID)
        cubeEdgeMappings[(0, i, UP)] = (totalRows - 1, i - 100, UP)
        cubeEdgeMappings[(totalRows - 1, i - 100, DOWN)] = (0, i, DOWN)

    # Face 1 right <-> face 4 right (upside-down)
    # Direction same both ways, R -> L or R -> L
    for i in range(0, 50):
        assert(data[i][totalCols - 1] != VOID)
        assert(data[149 - i][99] != VOID)
        cubeEdgeMappings[(i, totalCols - 1, RIGHT)] = (149 - i, 99, LEFT)
        cubeEdgeMappings[(149 - i, 99, RIGHT)] = (i, totalCols - 1, LEFT)

    # Face 1 bottom <-> face 3 right
    # Direction D -> L or R -> U
    for i in range(100, 150):
        assert(data[49][i] != VOID)
        assert(data[i - 50][99] != VOID)
        cubeEdgeMappings[(49, i, DOWN)] = (i - 50, 99, LEFT)
        cubeEdgeMappings[(i - 50, 99, RIGHT)] = (49, i, UP)

    # Face 2 left <-> face 5 left (upside-down)
    # Direction same both ways, L -> R or L -> R
    for i in range(0, 50):
        assert(data[i][50] != VOID)
        assert(data[149 - i][0] != VOID)
        cubeEdgeMappings[(i, 50, LEFT)] = (149 - i, 0, RIGHT)
        cubeEdgeMappings[(149 - i, 0, LEFT)] = (i, 50, RIGHT)

    # Face 3 left <-> face 5 top
    # Direction: L -> D or U -> R
    for i in range(50, 100):
        assert(data[i][50] != VOID)
        assert(data[100][i - 50] != VOID)
        cubeEdgeMappings[(i, 50, LEFT)] = (100, i - 50, DOWN)
        cubeEdgeMappings[(100, i - 50, UP)] = (i, 50, RIGHT)

    # Face 4 bottom <-> face 6 right
    # Direction: D -> L or R -> U
    for i in range(50, 100):
        assert(data[149][i] != VOID)
        assert(data[i + 100][49] != VOID)
        cubeEdgeMappings[(149, i, DOWN)] = (i + 100, 49, LEFT)
        cubeEdgeMappings[(i + 100, 49, RIGHT)] = (149, i, UP)

    return cubeEdgeMappings


'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve(isCube=False):
    # Set up full grid (extend space if cut short of max width)
    grid = [line + [' ' for i in range(totalCols - len(line))] for line in data]

    # Set up cube config for sol 2s
    cubeEdgeMappings = None if not isCube else setUpCubeMappings()
    cubeConfig = (isCube, cubeEdgeMappings)

    # Set initial position to the first path point in the top left row, starting from (0, 0)
    row, col, _ = getNextPosition(grid, 0, 0, RIGHT, cubeConfig)
    start = (row, col)

    # Default looking up, such that we adjust to starting position of RIGHT on first parse
    facing = UP

    # Perform movements while accounting for direction facing, especially for sol 2 where
    # flipping the cube entails changing direction mid-movement and working off the new
    # direction in future movements
    for idx, movement in enumerate(movements):
        row, col, facing = move(grid, row, col, movement, facing, cubeConfig)

    # Final key is 1000 * row + 4 * col + facing, be sure to add 1 to row and col since we
    # work in 0-indexed grid, and they expect a 1-indexed answer
    key = sum([1000 * (row + 1), 4 * (col + 1), facing])

    if DEBUG:
        print(f"Starting at position {start}, final position = ({row + 1}, {col + 1}), facing = {arrows[facing]} or {facing}, final key = {key}\n")

    return key

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
data = [[*line] for line in [line.rstrip() for line in sys.stdin.readlines()] if line != '']

# Set initial direction to right
movements = [(direction, int(steps)) for direction, steps in re.findall('([A-Z])([0-9]+)', 'R' + ''.join(data.pop()))]
totalRows, totalCols = len(data), max([len(x) for x in data])s

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1 = solve()

# Skip test case for sol 2
sol2 = solve(True) if len(movements) > 20 else "Skipped"

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
