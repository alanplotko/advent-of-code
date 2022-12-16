import sys, time, re, math

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def getDiagonalPath(src, dst, min, max):
    x1, y1 = src
    x2, y2 = dst
    newSrc = None
    path = []
    while newSrc != dst:
        if x2 > x1:
            x1 += 1
        else:
            x1 -= 1
        if y2 > y1:
            y1 += 1
        else:
            y1 -= 1
        newSrc = tuple([x1, y1])
        # Add point if within range [min, max] for x1 and y1
        if x1 >= min and x1 <= max and y1 >= min and y1 <= max:
            path.append(newSrc)
    return path

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
# Measure manhattan distance between every sensor and potential beacon point
# and compare with the sensor's closest beacon. If the potential beacon's
# distance <= sensor's closest distance, then we know that is not possible,
# so we mark that point as '#' to note that it's not a valid beacon location.
def solveSol1(y):
    # Increase search area by y
    min = minX - y
    max = maxX + y

    # Track existing beacons in row y
    existingBeacons = set([beacon[0] for beacon in beacons if beacon[1] == y])

    # Track beacon placement in row
    row = ['.' for i in range(max - min)]

    # Shift for accessing 0-index list
    shift = 0 - min if min < 0 else -1 * (min - 0)

    if DEBUG:
        print(existingBeacons, flush=True)
        print(shift, flush=True)

    # Check entire x range +/- y
    for i in range(min, max):
        idx = i + shift
        if i in existingBeacons:
            row[idx] = 'B'
            continue
        canPlaceBeacon = True
        for j in range(len(sensors)):
            dist = manhattan_distance(sensors[j], tuple([i, y]))
            if dist <= dists[j]:
                canPlaceBeacon = False
                break

            if DEBUG:
                print(f'{sensors[j]} -> {beacons[j]} = {dists[j]} ; {sensors[j]} -> {tuple([i, y])} = {dist} ; result = {dist <= dists[j]}')

        if not canPlaceBeacon:
            row[idx] = '#'

    return len([x for x in row if x == '#'])

# Limit to range [0, 4000000] and search all points for the single distress
# beacon. However, this is not performant, as we'd then brute force a check of
# 4MM * 4MM points! However, we can instead look at the example and see that
# the point happened to be right outside the perimeter! Let's check all points
# that are 1 away from the covered diamond-shaped area. This cuts down our points
# to check significantly, especially since we can ignore any points outside
# the bounds of [0, 4000000].
def solveSol2(min, max):
    totalPoints = (max - min) * (max - min)
    pointsCheckedUntilFound = 0
    for idx, sensor in enumerate(sensors):
        # Add 1 to each x or y to ensure we're checking outside the perimeter
        coords = [
            tuple([sensor[0] + dists[idx] + 1, sensor[1]]), # Rightmost point + 1
            tuple([sensor[0], sensor[1] - dists[idx] - 1]), # Topmost point + 1
            tuple([sensor[0] - dists[idx] - 1, sensor[1]]), # Leftmost point + 1
            tuple([sensor[0], sensor[1] + dists[idx] + 1])  # Bottommost point + 1
        ]

        if DEBUG:
            print(f'{sensor}: {coords}', flush=True)

        for i in range(len(coords)):
            # Get src -> dst, loop back to starting point using % to complete
            # the perimeter check across all 4 points of the diamond
            src = coords[i]
            dst = coords[(i + 1) % len(coords)]

            # Recursively generate path of all eligible points from src -> dst
            eligiblePoints = getDiagonalPath(src, dst, min, max)
            pointsCheckedUntilFound += len(eligiblePoints)

            if DEBUG:
                print(f'Checking {len(eligiblePoints)} targets', flush=True)

            for point in eligiblePoints:
                canPlaceBeacon = True
                for x in range(len(sensors)):
                    dist = manhattan_distance(sensors[x], point)
                    if dist <= dists[x]:
                        canPlaceBeacon = False
                        break
                if DEBUG:
                    print(f'Processed {point} -> {dst}', flush=True)
                if canPlaceBeacon:
                    if DEBUG:
                        print(f'Can place beacon at {point}', flush=True)
                    return ((point[0] * 4000000) + point[1], totalPoints, pointsCheckedUntilFound)
    return (None, totalPoints, pointsCheckedUntilFound)

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
data = [line.rstrip() for line in sys.stdin.readlines()]
matches = [re.findall(r'x=(-?\d+),\s+y=(-?\d+)', line) for line in data]

# Track sensors and beacons
sensors = [tuple([int(pair[0][0]), int(pair[0][1])]) for pair in matches]
beacons = [tuple([int(pair[1][0]), int(pair[1][1])]) for pair in matches]

# Get manhattan distance per pair of sensors and beacons
dists = [manhattan_distance(sensors[i], beacons[i]) for i in range(len(sensors))]

# Determine bounds for x
xs = [x[0] for x in (sensors + beacons)]
minX = min(xs)
maxX = max(xs)

if DEBUG:
    print(f'Min x = {minX}, max x = {maxX}')
    print(sensors)
    print(beacons)

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
# Arguments provided by problem directly this time around instead of via input.
# Assess whether to use test case based on largest X value encountered. For
# the test case, all xs are < 100, and larger otherwise for the problem input.
sol1 = solveSol1(10 if maxX < 100 else 2000000)

beaconLocation, totalPoints, pointsCheckedUntilFound = solveSol2(0, 20 if maxX < 100 else 4000000)
sol2 = beaconLocation

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}, stats: found solution in {pointsCheckedUntilFound:,} points, narrowed down from {totalPoints:,} total points")
