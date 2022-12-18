import sys, time
from collections import deque
from operator import add

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# Get all neighbors for point in bounds [0, maxBound). If restricting to input data, filter out points not in input data.
def getNeighbors(point, maxBound):
    return [
        neighbor for movement in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        if max((neighbor := tuple(map(add, point, movement)))) < maxBound and min(neighbor) >= 0
    ]

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    # Get maximum bound for x, y, or z
    maxBound = max([max(x) for x in data.keys()]) + 1

    # Generate 3d grid for solution 2 initialized to air = 0 if point not in input, or lava = 1 if point in input
    grid = {point: (1 if point in data else 0) for point in [(x, y, z) for x in range(maxBound) for y in range(maxBound) for z in range(maxBound)]}

    # Precompute all neighbors for grid
    allNeighbors = {point: getNeighbors(point, maxBound) for point in grid}

    # Get all lava points' neighbors that are also in input data
    # Optimization: O(1) lookups against dict where marked as lava = 1 vs. checking if point present in list
    lavaNeighbors = {point: [neighbor for neighbor in allNeighbors[point] if grid[neighbor] == 1] for point in data.keys()}

    '''
    Solution 1
    '''
    maxFaces = len(data) * 6
    intersections = sum([len(x) for x in lavaNeighbors.values()])
    surfaceArea = maxFaces - intersections

    '''
    Solution 2
    '''
    # Start at origin for running floodfill
    floodfill = deque([(0, 0, 0)])
    visited = {} # O(1) lookups in dict for performance

    # Floodfill where air = 0 to water = -1
    while floodfill:
        point = floodfill.popleft()
        if max(point) >= maxBound:
            continue
        if grid[point] == 0:
            grid[point] = -1
            # Traverse through unvisited neighbors to find next locations for floodfill
            unvisited = [neighbor for neighbor in allNeighbors[point] if neighbor not in visited]
            for neighbor in unvisited:
                floodfill.append(neighbor)
                visited[neighbor] = True

    # Subtract sum of overcounted faces from total
    overCounted = 0

    # Get all points where air = 0
    airPockets = [point for point,value in grid.items() if value == 0]
    for point in airPockets:
        overCounted += sum([grid[neighbor] for neighbor in allNeighbors[point]])

    return (surfaceArea, surfaceArea - overCounted)

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
# Parse data as dict for fast O(1) lookups
data = {tuple(map(int, x)): True for x in [x.split(",") for x in [line.rstrip() for line in sys.stdin.readlines()]]}

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1, sol2 = solve()

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
