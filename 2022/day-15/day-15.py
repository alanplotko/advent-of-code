import sys, time, re, math

'''''''''''''''''''''
SETUP
'''''''''''''''''''''

# Print statements
DEBUG = False
TRACE = False

'''''''''''''''''''''
DATA PARSING
'''''''''''''''''''''

# Parse data
data = [line.rstrip() for line in sys.stdin.readlines()]
matches = [re.findall(r'x=(-?\d+),\s+y=(-?\d+)', line) for line in data]
sensors = [tuple([int(pair[0][0]), int(pair[0][1])]) for pair in matches]
beacons = [tuple([int(pair[1][0]), int(pair[1][1])]) for pair in matches]
xs = [x[0] for x in (sensors + beacons)]
minX = min(xs)
maxX = max(xs)
if DEBUG: print(f'Min x = {minX}, max x = {maxX}')
if DEBUG: print(sensors)
if DEBUG: print(beacons)

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

dists = [manhattan_distance(sensors[i], beacons[i]) for i in range(len(sensors))]

def moveDiagonal(src, dst, min, max):
    x1, y1 = src
    x2, y2 = dst
    goodCoord = True
    newSrc = None
    targets = []
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
        targets.append(newSrc)
    return targets

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''

def solveSol1(y):
    # Increase search area by y
    min = minX - y
    max = maxX + y
    existingBeacons = set([beacon[0] for beacon in beacons if beacon[1] == y])
    row = ['.' for i in range(max - min)]
    shift = 0 - min if min < 0 else -1 * (min - 0)
    if DEBUG: print(existingBeacons, flush=True)
    if DEBUG: print(shift, flush=True)
    for i in range(min, max):
        idx = i + shift
        if i in existingBeacons:
            row[idx] = 'B'
            continue
        eligibleSpot = True
        for j in range(len(sensors)):
            dist = manhattan_distance(sensors[j], tuple([i, y]))
            if DEBUG: print(f'{sensors[j]} -> {beacons[j]} = {dists[j]} ; {sensors[j]} -> {tuple([i, y])} = {dist} ; result = {dist < dists[j]}')
            if dist <= dists[j]:
                eligibleSpot = False
        if not eligibleSpot:
            row[idx] = '#'

    return len([x for x in row if x == '#'])

def solveSol2(minBound, maxBound):
    for idx, sensor in enumerate(sensors):
        coords = [tuple([sensor[0] + dists[idx] + 1, sensor[1]]), tuple([sensor[0], sensor[1] - dists[idx] - 1]), tuple([sensor[0] - dists[idx] - 1, sensor[1]]), tuple([sensor[0], sensor[1] + dists[idx] + 1])]
        if DEBUG: print(f'{sensor}: {coords}', flush=True)
        for i in range(len(coords)):
            src = coords[i]
            dst = coords[(i + 1) % len(coords)]
            done = False
            targets = moveDiagonal(src, dst, minBound, maxBound)
            eligible = [x for x in targets if x[0] >= minBound and x[0] <= maxBound and x[1] >= minBound and x[1] <= maxBound]
            if DEBUG: print(f'Checking {len(eligible)} targets', flush=True)
            for target in eligible:
                eligibleSpot = True
                for x in range(len(sensors)):
                    dist = manhattan_distance(sensors[x], target)
                    if dist <= dists[x]:
                        eligibleSpot = False
                        break
                if eligibleSpot:
                    if DEBUG: print(target, flush=True)
                    return (target[0] * 4000000) + target[1]
                if DEBUG: print(f'Processed {target} -> {dst}', flush=True)
    return None

'''''''''''''''''''''
LOG SOLUTIONS
'''''''''''''''''''''

startTime = time.time()
sol1 = solveSol1(2000000)
print(f"--- Ran for {(time.time() - startTime)} seconds ---")

startTime = time.time()
sol2 = solveSol2(0, 4000000)
print(f"--- Ran for {(time.time() - startTime)} seconds ---")

print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
