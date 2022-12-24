import sys, time

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
ELF, GROUND = '#', '.'
directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

# Print grid for visualization purposes. Useful for debugging.
def printGrid(grid, bounds=None):
    if bounds == None:
        for row in grid:
            print(f"{''.join(row)}")
    else:
        top, bottom, left, right = bounds
        for row in grid[top:bottom + 1]:
            print(f"{''.join(row[left:right + 1])}")

# Get minimum bounds containing all elves
def getBounds(grid):
    rows = [elf[0] for elf in grid.keys()]
    cols = [elf[1] for elf in grid.keys()]
    return (min(rows), max(rows), min(cols), max(cols))

# Get neighbors for position (r, c) if there is at least 1 elf neighbor, else return empty list
def getNeighbors(grid, r, c):
    neighbors = {}
    for direction in directions:
        row, col = r, c
        if 'N' in direction:
            row -= 1
        if 'S' in direction:
            row += 1
        if 'W' in direction:
            col -= 1
        if 'E' in direction:
            col += 1
        neighbors[direction] = (row, col)

    hasAdjacentElf = any([neighbor in grid for neighbor in neighbors.values()])

    if DEBUG:
        print(f"Elf at ({r}, {c}), has elf neighbor = {hasAdjacentElf}, neighbors = {neighbors}")

    return {k: v for k, v in neighbors.items() if v not in grid} if hasAdjacentElf else {}

# Perform movement for round
def move(grid, roundNumber, endAtNoNeighbors, phases):
    if DEBUG:
        print(f"== Round {roundNumber} ==\n")

    # Store map of dst -> elf src
    proposedMovements = {}
    seen = set()

    for elf in grid.keys():
        row, col = elf
        # For each elf, get eligible neighbors if they have at least 1 elf neighbor
        neighbors = getNeighbors(grid, elf[0], elf[1])
        # Skip movement if no elf neighbors
        if neighbors:
            # If no phase is fulfilled, then the elf does not move
            for direction, phase in enumerate(phases):
                if all(key in neighbors for key in phase):
                    if DEBUG:
                        print(f"Condition met at phase {direction}: {phase}")
                    if phase[0] == 'N':
                        proposedMovements[(row, col)] = (row - 1, col)
                    elif phase[0] == 'S':
                        proposedMovements[(row, col)] = (row + 1, col)
                    elif phase[0] == 'W':
                        proposedMovements[(row, col)] = (row, col - 1)
                    else:
                        proposedMovements[(row, col)] = (row, col + 1)
                    break

    # Remove elf movements sharing dst point
    seen, duplicates = set(), set()
    for src, dst in proposedMovements.items():
        if dst in seen:
            duplicates.add(dst)
        else:
            seen.add(dst)

    if DEBUG:
        print(f"Movements = {proposedMovements}, seen = {seen}, duplicates = {duplicates}")

    # Track if elves moved this round
    moved = False

    # Perform movements where dst was unique
    for src, dst in proposedMovements.items():
        if dst not in duplicates:
            moved = True
            del grid[src]
            grid[dst] = ELF

    # Move first direction to consider each round to the end of the phase list
    phases.append(phases.pop(0))

    # Return moved status for sol 2
    return moved

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve(rounds=10, endAtNoNeighbors=False):
    grid = {}
    phases = [('N', 'NE', 'NW'), ('S', 'SE', 'SW'), ('W', 'NW', 'SW'), ('E', 'NE', 'SE')]

    # Convert unbounded grid to dict of points
    for row, r in enumerate(data):
        for col, c in enumerate(data[row]):
            if data[row][col] == ELF:
                grid[(row, col)] = ELF

    # For sol 2, we only want the round number where no elves moved
    if endAtNoNeighbors:
        done = False
        roundNumber = 1
        while not done:
            moved = move(grid, roundNumber, endAtNoNeighbors, phases)
            if not moved:
                return roundNumber
            roundNumber += 1
    # For sol 1, we move only a certain number of rounds and then compute the unoccupied area (ground)
    else:
        for i in range(rounds):
            move(grid, i + 1, endAtNoNeighbors, phases)

        # Get the bounds where elves occupy the space
        bounds = getBounds(grid)
        top, bottom, left, right = bounds

        if DEBUG:
            print(bounds)

        # Area of rectangle - # of elves = unoccupied space (ground)
        return (abs(bottom - top + 1) * abs(right - left + 1)) - len(grid)

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

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1 = solve()
sol2 = solve(endAtNoNeighbors=True)

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
