import sys, time, re, math

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
def translate_locations(seeds, mapping):
    locations = {}
    for seed in seeds:
        locations[seed] = translate_location(seed, mapping)
    return locations

# For sol 1
def translate_location(seed, mapping):
    locations = {}
    translation = seed
    if TRACE:
        path = str(seed)
    for idx, item in enumerate(mapping):
        for coord in item['coords']:
            start, end, offset, skip = coord
            if TRACE:
                found = False
            if start <= translation <= end:
                translation -= offset
                if TRACE:
                    found = True
                    path += f"\t->\t{translation}"
                break
        if TRACE and not found:
            path += f"\t->\t{translation}"
    if TRACE:
        print(path)
    return translation

# For sol 2
def translate_location_optimized(seed, mapping, mark_skipped=False):
    locations = {}
    translation = seed
    if TRACE:
        path = str(seed)
    prev_mapping_idx = None
    prev_coord_idx = None
    for mapping_idx, item in enumerate(mapping):
        for coord_idx, coord in enumerate(item['coords']):
            start, end, offset, skip = coord
            if TRACE:
                found = False
            if start <= translation <= end:
                if skip:
                    mapping[prev_mapping_idx]['coords'][coord_idx][3] = True
                    path += f"\t->\t SKIP"
                    print(path)
                    return None
                elif mark_skipped and mapping_idx == len(mapping) - 1:
                    item['coords'][coord_idx][3] = True
                    path += f"\t->\t SKIP"
                    print(path)
                    return None
                prev_mapping_idx = mapping_idx
                prev_coord_idx = coord_idx
                translation -= offset
                if TRACE:
                    found = True
                    path += f"\t->\t{translation}"
                break
        if TRACE and not found:
            path += f"\t->\t{translation}"
    if TRACE:
        print(path)
    return translation

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    seeds_sol1 = []
    mapping = []
    idx = -1

    for row in data:
        if 'seeds' in row:
            seeds_sol1 = list(map(int, row.split(': ')[1].split()))
        elif 'map' in row:
            idx += 1
            mapping.append({ 'name': row.split(' map:')[0], 'coords': [] })
        else:
            dst, src, count = list(map(int, row.split()))
            # Start, end, offset to subtract to translate to new map, whether to skip coordinate (for eliminating paths in sol 2)
            coord = [src, src + count - 1, src - dst, False]
            mapping[idx]['coords'].append(coord)

    # locations_sol1 = translate_locations(seeds_sol1, mapping)

    minimum_location = float('inf')
    skip = []
    for i in range(0, len(seeds_sol1) - 1, 2):
        start, end = seeds_sol1[i:i+2]
        current = float('inf')
        last_seen = float('inf')
        mark_skipped = False
        for j in range(start, start + end):
            if current != None:
                last_seen = current
            if (mark_skipped):
                print("Skipping")
            current = translate_location_optimized(j, mapping, mark_skipped)
            if current != None and current < minimum_location:
                minimum_location = current
            if current != None and current > last_seen:
                mark_skipped = True

    if DEBUG:
        for row in mapping:
            print(row)
    return None, minimum_location #min(locations_sol1.values()), minimum_location

'''''''''''''''''''''
SETUP
'''''''''''''''''''''
# Print statements
DEBUG = True
TRACE = True

# Start timer
startTime = time.time()

'''''''''''''''''''''
DATA PARSING
'''''''''''''''''''''
# Parse data
data = [line.rstrip() for line in sys.stdin.readlines() if line.rstrip()]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1, sol2 = solve()

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
