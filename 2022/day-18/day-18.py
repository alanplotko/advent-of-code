import sys, time
from collections import deque

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# Get neighbors for point within [0, maxBound) from all points (filterToDataOnly=False) or only
# points from input data (filterToDataOnly=True)
def getNeighbors(point, maxBound, filterToDataOnly=False):
    x, y, z = point
    neighbors = [
        (x + dx, y + dy, z + dz)
        for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        if y + dy in range(maxBound) and x + dx in range(maxBound) and z + dz in range(maxBound)
    ]
    # Filter out points not in data if filterToDataOnly = True, otherwise return all
    # possible neighbors for floodfill
    return [point for point in neighbors if point in data] if filterToDataOnly else neighbors

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    # Get maximum bound for x, y, or z
    maxBound = max([max(x) for x in data]) + 1

    '''
    Solution 1
    '''
    # Get neighbors for point in data where also present in data
    neighbors = {point: getNeighbors(point, maxBound, True) for point in data}
    maxFaces = len(data) * 6
    intersections = sum(len(x) for x in neighbors.values())
    surfaceArea = maxFaces - intersections

    '''
    Solution 2
    '''

    # Generate 3d grid initialized to air = 0 if point not in input, or lava = 1 if point in input
    grid = {point: (1 if point in data else 0) for point in [(x, y, z) for x in range(maxBound) for y in range(maxBound) for z in range(maxBound)]}

    # Start at origin for running floodfill
    floodfill = deque([(0, 0, 0)])
    visited = {}

    # Floodfill where air = 0 to water = -1
    while floodfill:
        point = floodfill.popleft()
        if max(point) >= maxBound:
            continue
        if grid[point] == 0:
            grid[point] = -1
            # Traverse through unvisited neighbors to find next locations for floodfill
            unvisited = [neighbor for neighbor in getNeighbors(point, maxBound) if neighbor not in visited]
            for neighbor in unvisited:
                floodfill.append(neighbor)
                visited[neighbor] = True

    # Subtract sum of overcounted faces from total
    overCounted = 0
    for point in grid.keys():
        if grid[point] == 0:
            # Get the values rather than the neighbors
            overCounted += sum([grid[neighbor] for neighbor in getNeighbors(point, maxBound)])

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
# Parse data
data = [tuple(map(int, x)) for x in [x.split(",") for x in [line.rstrip() for line in sys.stdin.readlines()]]]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1, sol2 = solve()

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
