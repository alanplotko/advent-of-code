import sys, time, re, math

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# Encountered error in tracking seed ranges, corrected by comparing with sample solution from Advent of Code Subreddit
# Important: reduce visit scope while translating ranges, especially given the input size
# Inspiration from sample solution to merge range exploration for both sol1 and sol2 (with sol1 just being a range of 1)
def translate_locations(seeds, mapping):
    # For each mapping table, we perform a translation for all seeds
    for item in mapping:
        ranges = []
        for seed in seeds:
            x1, x2 = seed
            # Reduce scope of ranges to check given large input if out of range
            for start, end, offset in item:
                if x1 < start:
                    # Full range out of scope, need to explore
                    if x2 <= start:
                        ranges.append((x1, x2))
                        seed = None
                        break
                    # Partial range out of scope, need to explore
                    else:
                        ranges.append((x1, start))
                        x1 = start
                # Perform translation if in range
                if start <= x1 < end:
                    ranges.append((x1 + offset, min(x2, end) + offset))
                    # x2 in range, so no need to explore
                    if x2 <= end:
                        seed = None
                        break
                    # x2 out of range, move x1 up to match and explore remaining partial range
                    else:
                        x1 = end
            # Add seed range if still valid to explore
            if seed != None:
                ranges.append(seed)
        seeds = ranges
    return seeds

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    # Parse seeds from input
    seed_data = list(map(int, data[0].split("seeds: ")[1].split()))

    # Parse seed ranges
    mapping = [[] for i in range(7)]
    idx = -1
    for item in data[1:]:
        if 'map' in item:
            idx += 1
        else:
            # Parse coords as list of ints
            coords = list(map(int, item.split()))

            # End, start, offset to subtract to translate back into the mapping
            end, start, offset = coords
            mapping[idx].append((start, start + offset, end - start))

    for i in range(len(mapping)):
        mapping[i].sort(key=lambda arr: arr[1])

    # Compute locations for given seeds
    seeds = [(location, location + 1) for location in seed_data]
    min_loc_sol1 = min(translate_locations(seeds, mapping))[0]

    # Compute locations for given seed ranges
    seeds = [(seed_data[num], seed_data[num] + seed_data[num + 1]) for num in range(0, len(seed_data) - 1, 2)]
    min_loc_sol2 = min(translate_locations(seeds, mapping))[0]

    return min_loc_sol1, min_loc_sol2

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
