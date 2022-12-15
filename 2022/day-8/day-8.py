import sys, math

# Parse tree grid as 2d array of ints
data = [list(map(int, x)) for x in [[*x] for x in [line.rstrip() for line in sys.stdin.readlines()]]]

# Derive perimeter for visible trees from edge
height = len(data)
width = len(data[0])
perimeterVisible = (height * 2) + (width * 2) - 4

# Helper functions to get trees in row or column
def top(arr, x, y):
    return [row[y] for row in arr[0:x]]

def bottom(arr, x, y):
    return [row[y] for row in arr[x+1:len(arr)]]

def left(arr, x, y):
    return arr[x][0:y]

def right(arr, x, y):
    return arr[x][y+1:len(arr)]

# Calculate scenic score by number of trees in path until a tree of matching or
# larger height blocks the view. That tree is also included in the count.
def calculateScenicScore(arr, height):
    count = 0
    for tree in arr:
        count +=1
        if tree >= height:
            break
    return count

# Count visible trees for solution 1
visibleCount = 0

# Track max scenic score for solution 2
maxScenicScore = 0

# Walk through tree grid
for x, row in enumerate(data):
    if x == 0 or x == len(row) - 1:
        continue
    for y, col in enumerate(row):
        if y == 0 or y == len(row) - 1:
            continue

        # Get trees in all directions from tree at (x, y). Optimization:
        # reversing top and left are needed for solution 2, as we go backward
        # to the edge. This won't impact solution 1, since we just need the max
        # height visible in that direction from tree at (x, y).
        directions = [
            top(data, x, y)[::-1],
            left(data, x, y)[::-1],
            bottom(data, x, y),
            right(data, x, y)
        ]

        # Get lowest encountered maximum from all directions
        height = data[x][y]
        lowestMax = min([max(x) for x in directions])

        # If at least one max < height, then we can count that tree as visible
        if lowestMax < height:
            visibleCount += 1

        # Calculate scenic score for tree at (x, y). We're skipping trees along
        # the perimeter in this iteration, and that's ok since they will zero
        # out for the product and match our initial max score of 0.
        maxScenicScore = max(
            # Get product of scenic scores across all directions
            math.prod([calculateScenicScore(x, height) for x in directions]),
            maxScenicScore
        )

        # For debugging
        # print("x = %d, y = %d, val = %d" % (x,y,data[x][y]))
        # print("left = %s, current value = %d" % (data[x][0:y], data[x][y]))
        # print("right = %s, current value = %d" % (data[x][y+1:len(data)], data[x][y]))
        # print("top = %s, current value = %d" % (top(data, x, y), data[x][y]))
        # print("bottom = %s, current value = %d" % (bottom(data, x, y), data[x][y]))
        # print("scenic score = %d, tree pos = (%d, %d)" % (score, x, y))

sol1 = perimeterVisible + visibleCount
sol2 = maxScenicScore

print("Part 1: " + str(sol1))
print("Part 2: " + str(sol2))
