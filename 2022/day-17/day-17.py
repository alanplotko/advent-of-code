import sys, time

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# Simple iterator that loops back to the start after reaching the end of the list
class LoopIterator:
    def __init__(self, elements):
        self.elements = elements
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        currentIndex = self.index
        self.index = (self.index + 1) % len(self.elements)
        return self.elements[currentIndex]

# Get entrance drop posigtion for a given block in the grid
def getEnteringPosition(grid):
    # Work up from the floor of the grid
    for idx, row in enumerate(grid[::-1]):
        if '#' not in row:
            # -1 for 0-indexed array, -3 for entrance buffer
            return len(grid) - idx - 4

# Left shift a block if no collisions with left edge
def leftShift(block):
    leftEdgeReachedLimit = '#' in [row[0] for row in block]
    return [row if leftEdgeReachedLimit else row[1:] + ['.'] for row in block]

# Right shift a block if no collisions with right edge
def rightShift(block):
    rightEdgeReachedLimit = '#' in [row[len(row) - 1] for row in block]
    return [row if rightEdgeReachedLimit else ['.'] + row[:-1] for row in block]

# Check if block can move down into a row that is already partially filled,
# if there's no blocks in the way
def canMoveDown(grid, block, proposedIndex):
    # False if going beyond the floor
    if proposedIndex >= len(grid):
        return False
    # If src unit is rock ("#") moving to dst already filled with rock ("#"),
    # then a shift is not possible
    for rowIdx in range(len(block)):
        for colIdx in range(len(block[rowIdx])):
            if block[len(block) - rowIdx - 1][colIdx] == '#' and grid[proposedIndex - rowIdx][colIdx] == '#':
                # Shift does not happen
                return False
    # No issues found, shift is possible
    return True

# Merge resulting block into the grid, keep any pre-existing rock locations in
# the grid, as that's been checked already by canMoveDown
def mergeRow(grid, rowIndex, row):
    for i in range(len(grid[rowIndex])):
        if grid[rowIndex][i] == '#':
            continue
        grid[rowIndex][i] = row[i]

# Get the tower's height by taking the difference of entrance position
# via getEnteringPosition and the floor (len(grid))
def getTowerHeight(grid):
    return len(grid) - (getEnteringPosition(grid) + 4)

# Print grid from entrance position to floor for visualization purposes.
# Useful for debugging.
def printGrid(grid):
    rowIndex = getEnteringPosition(grid)
    for row in grid[rowIndex:]:
        print(f"|{''.join(row)}|")
    print(f"+-------+\n")

# Construct a map of potential cycles, how often they happened, and the indices
# at which they started.
def constructCycleMap(lst, chunkSize):
    cycleMap = {}

    for i in range(0, len(lst), chunkSize):
        chunk = tuple(lst[i:i+chunkSize])

        if DEBUG:
            print(f"Chunk: {chunk}")

        if chunk in cycleMap:
            cycleMap[chunk]['count'] += 1
            cycleMap[chunk]['indices'].append(i)
        else:
            cycleMap[chunk] = { 'count': 1, 'indices': [i] }

    return cycleMap

# Find all possible patterns from list and return the pattern that recurred
# most frequently. May need to increase boundary size to locate the pattern.
def findPattern(lst):
    possible = {}
    for i in range(len(lst)):
        start = lst[i]
        end = lst[len(lst) - 1]
        for j in range(i + 1, len(lst)):
            candidate = lst[j]
            diff = candidate - start
            counter = start
            patternConsistent = True
            loopTimes = 0
            while counter + diff <= end:
                counter += diff
                loopTimes += 1
                if counter not in lst:
                    patternConsistent = False
                    break
            if patternConsistent:
                if DEBUG:
                    print(f"Start = {start}, candidate = {candidate}, diff = {diff}, loop times = {loopTimes}")
                possible[(start, candidate)] = loopTimes
    return max(possible, key=possible.get)

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve(n):
    '''
    Setup
    '''
    # Choose sizable boundary for finding patterns for solution 2. Arguments
    # provided by problem directly this time around instead of via input.
    # Assess whether to use test case boundary based on input length. For
    # the test case, we have 40 characters, and larger otherwise for
    # the problem input. # Add 1 to capture the tower height at n block drops.
    boundary = (n if len(data) < 100 else n * 3) + 1

    # Tallest rock is 4 units * boundary rocks to work with. We'll collect
    # the tower height for solution 1 during iteration when = n blocks
    grid = [['.' for x in range(7)] for x in range(boundary * 4)]

    # Set up iterators for jets and blocks
    jets = LoopIterator(data)
    blocks = LoopIterator([
        # Dash
        [
            ['.', '.', '#', '#', '#', '#', '.']
        ],
        # Plus
        [
            ['.', '.', '.', '#', '.', '.', '.'],
            ['.', '.', '#', '#', '#', '.', '.'],
            ['.', '.', '.', '#', '.', '.', '.']
        ],
        # Backwards L
        [
            ['.', '.', '.', '.', '#', '.', '.'],
            ['.', '.', '.', '.', '#', '.', '.'],
            ['.', '.', '#', '#', '#', '.', '.']
        ],
        # Vertical line
        [
            ['.', '.', '#', '.', '.', '.', '.'],
            ['.', '.', '#', '.', '.', '.', '.'],
            ['.', '.', '#', '.', '.', '.', '.'],
            ['.', '.', '#', '.', '.', '.', '.']
        ],
        # Square box
        [
            ['.', '.', '#', '#', '.', '.', '.'],
            ['.', '.', '#', '#', '.', '.', '.'],
        ]
    ])

    # Track deltas in tower height growth as we drop each block to help find
    # patterns in solution 2. We are always following the same movements in
    # block drops and jets, so there's bound to be a pattern to derive the
    # height at n block drops without manually simulating all n block drops.
    deltas = []
    prevDelta = 0
    nextDelta = 0

    if TRACE:
        print("=== Starting Position ===")
        printGrid(grid)

    # Track tower height at n blocks for solution 1
    towerHeight = 0

    '''
    Simulate Tetris
    '''

    # Simulate up to boundary
    for i in range(boundary):
        # Derive next block to drop
        nextBlock = next(blocks)

        # Record tower height if at n blocks before proceeding
        if i == n:
            towerHeight = nextDelta

        # Get position we're dropping from
        rowIndex = getEnteringPosition(grid)

        # Print out Tetris visualization
        if DEBUG:
            print(f"=== Round {i + 1} ===", flush=True)
        if TRACE:
            print(f"Entering position = {rowIndex}\n")
            printGrid(grid)
            # Print starting position of nextBlock
            print("Current Block:")
            for row in nextBlock:
                print(''.join(row))
            print() # Newline

        # Process the left and right movements as we drop down by 4 rows
        for steps in range(4):
            nextJet = next(jets)
            if nextJet == '<':
                nextBlock = leftShift(nextBlock)
            else:
                nextBlock = rightShift(nextBlock)

            if TRACE:
                print(f"{nextJet}:")
                for row in nextBlock:
                    print(''.join(row))
                print() # Newline

        if TRACE:
            print() # Newline
            print(f"Place on {rowIndex + 3}")

        # Adjust row index since we've dropped down from the entrance point
        rowIndex += 3

        # Check if bottom of block can fall further
        checkMovement = True
        while checkMovement:
            proposedIndex = rowIndex + 1
            checkMovement = canMoveDown(grid, nextBlock, proposedIndex)

            # If movement is possible, then we need to adjust row index and process the next jet
            if checkMovement:
                rowIndex += 1

                # At this point, since we know we can move down, we now have
                # to process the next jet
                nextJet = next(jets)
                if nextJet == '<':
                    proposedBlock = leftShift(nextBlock)
                else:
                    proposedBlock = rightShift(nextBlock)

                if TRACE:
                    print(f"Can move down, checking jet\n{nextJet}:")
                    for row in proposedBlock:
                        print(''.join(row))

                # Set block to proposed block if shift is possible without
                # a collision, otherwise return the same block
                canShift = canMoveDown(grid, proposedBlock, proposedIndex)
                if canShift:
                    nextBlock = proposedBlock

                if TRACE:
                    print(f"Moved down to {rowIndex}, canShift result for {nextJet} = {canShift}")

        # Now that we maximized how far we can drop without collision, merge
        # the final result to the grid
        for row in nextBlock[::-1]:
            mergeRow(grid, rowIndex, row)
            rowIndex -= 1

        # Print current result if visualizing
        if TRACE:
            printGrid(grid)

        # Track growth of tower height for each drop to help find patterns
        # for solution 2
        prevDelta = nextDelta
        nextDelta = getTowerHeight(grid)
        deltas.append(nextDelta - prevDelta)

    '''
    Find cycle for solution 2 to help calculate for 1000000000000 block drops
    '''

    # Construct cycle map by iterating over deltas in chunks of 5. Derived 5
    # from observing the test case growth deltas. You want a sizable amount for
    # finding patterns, without getting too big. The pattern is presumably
    # larger in real input vs. test case, so 5 is a good starting point.
    cycleMap = constructCycleMap(deltas, 5)

    # Find most recurring cycle of 5 growth deltas
    maxCycle = None
    maxCycleCount = 0
    for key, value in cycleMap.items():
        if DEBUG:
            print(key, value)
        if value['count'] > maxCycleCount:
            maxCycleCount = value['count']
            maxCycle = key
    if DEBUG:
        print(f"{maxCycle}: {maxCycleCount} at indices {cycleMap[maxCycle]['indices']}")

    # Find the start and end index for the most frequent repeating pattern
    startIndex, endIndex = findPattern(cycleMap[maxCycle]['indices'])

    # Slice our growth deltas to extract that pattern
    pattern = deltas[startIndex:endIndex]

    # Leaving aside the initial number of growth deltas outside of the
    # repeating pattern, we have to walk through the rest to 1 trillion!
    remaining = 1000000000000 - startIndex

    # Total height is the sum of growth deltas at 0 -> startIndex before
    # the repeating pattern and however far we can get with the sum of
    # the pattern as we make our way to 1 trillion. The remaining amount of
    # drops to simulate, x, can come from the sum of the first x growth deltas.
    totalHeight = sum(deltas[0:startIndex]) + \
        (sum(pattern) * (remaining // len(pattern))) + \
        sum(pattern[:(remaining % len(pattern))])

    # Return solution 1, the tower height at n blocks drops, and solution 2,
    # the total height derived for 1 trillion block drops
    return (towerHeight, totalHeight)

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
data = [*sys.stdin.readline().rstrip()]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1, sol2 = solve(2022)

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
