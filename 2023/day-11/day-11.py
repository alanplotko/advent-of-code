import sys, time, re, math, itertools

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
def parse_grid(arr):
    return [list(x) for x in [[*x] for x in arr]]

# Expand each galaxy by the count of empty rows or columns preceding the x/y coordinate
def expand_space(galaxies, expand_size, empty_rows, empty_cols):
    expand_size = expand_size - 1 if expand_size > 1 else 1
    return [(x + (expand_size * len([row for row in empty_rows if x > row])), y + (expand_size * len([col for col in empty_cols if y > col]))) for (x, y) in galaxies]

# Path distance can be calculated by the absolute sum of differences in x/y coordinates
def compute_dist(coords):
    return [abs(x2 - x1) + abs(y2 - y1) for (x1, y1), (x2, y2) in coords]

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    grid = parse_grid(data)

    # Compute rows and columns without galaxies
    empty_rows = [idx for idx, row in enumerate(grid) if len(list(set(row))) == 1 and list(set(row))[0] == '.']
    empty_cols = [idx for idx, col in enumerate([list(col) for col in zip(*grid)]) if len(list(set(col))) == 1 and list(set(col))[0] == '.']

    # Get galaxy coordinates marked with "#"
    galaxies = [(row, col) for col, _ in enumerate(grid) for row, _ in enumerate(grid) if grid[row][col] == '#']

    # Get translated coordinates after expansion
    galaxies_sol1 = expand_space(galaxies, 1, empty_rows, empty_cols)
    galaxies_sol2 = expand_space(galaxies, 1000000, empty_rows, empty_cols)

    # Compute sum of shortest distances between every pair of coordinates
    return sum(compute_dist(list(itertools.combinations(galaxies_sol1, 2)))), sum(compute_dist(list(itertools.combinations(galaxies_sol2, 2))))

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

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1, sol2 = solve()

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
