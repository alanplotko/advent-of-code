import sys, time, re

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''

# Parse grid for computing neighbors
def parse_grid(arr):
    return [list(x) for x in [[*x] for x in arr]]

# Get all neighbors including diagonal
def get_all_neighbors(arr, row, col):
    adjacent = [
        [(row-1, col), arr[row-1][col]] if row - 1 >= 0 else None,                                                  # Top
        [(row-1, col+1), arr[row-1][col+1]] if row - 1 >= 0 and col + 1 <= len(arr[row]) else None,                 # Top Right
        [(row, col+1), arr[row][col+1]] if col + 1 <= len(arr[row]) - 1 else None,                                  # Right
        [(row+1, col+1), arr[row+1][col+1]] if row + 1 <= len(arr[row]) - 1 and col + 1 <= len(arr[row]) else None, # Bottom Right
        [(row+1, col), arr[row+1][col]] if row + 1 <= len(arr[row]) - 1 else None,                                  # Bottom
        [(row+1, col-1), arr[row+1][col-1]] if row + 1 <= len(arr[row]) - 1 and col - 1 >= 0 else None,             # Bottom Left
        [(row, col-1), arr[row][col-1]] if col - 1 >= 0 else None,                                                  # Left
        [(row-1, col-1), arr[row-1][col-1]] if row - 1 >= 0 and col - 1 >= 0 else None                              # Top Left
    ]
    return [x for x in adjacent if x[1] != None and x[1].isdigit()]

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    total = 0       # Sol 1 tracking
    product = 0     # Sol 2 tracking

    # Precompute number locations using regex per line
    numbers = {}
    for row_number, row in enumerate(data):
        matches = re.finditer('(\d+)', row)
        numbers[row_number] = list(matches)

    # Parse data as grid for computing neighbors when iterating for symbols
    # Alternatively can precompute symbol locations using regex just as with the numbers
    grid = parse_grid(data)
    neighbors = {}
    for row_number, row in enumerate(grid):
        for col_number, col in enumerate(row):
            if not col.isdigit() and col != '.':
                neighbors[(col, row_number, col_number)] = get_all_neighbors(data, row_number, col_number)

    parts_seen = set()     # For counting the valid parts for sol 1
    symbol_part_map = {}   # For counting the valid parts with exactly 2 matches for sol 2

    # For every match found for a symbol, dedupe by the whole number and not the individual neighboring digit in the grid
    #   - For sol 1: Dedupe matches in a set and sum them up
    #   - For sol 2: Track matches by their neighoring symbol, and for gears (* symbols with exactly 2 matches), sum their products
    for symbol, matches in neighbors.items():
        symbol_part_map[symbol] = []
        for match in matches:
            row, col = match[0]
            for number in numbers[row]:
                x, y = number.span()
                # Note y in span range is exclusive
                if x <= col < y:
                    # Track unique part for symbol
                    if number not in parts_seen:
                        symbol_part_map[symbol].append(number)
                    parts_seen.add(number)
                    break

    # Sum all numbers with a neighboring symbol
    for symbol, parts in symbol_part_map.items():
        for part in parts:
            total += int(part.group())

    # Sum all products of gears (* symbols with exactly 2 matches)
    for (char, _, _), matches in symbol_part_map.items():
        if char == '*' and len(matches) == 2:
            product += (int(matches[0].group()) * int(matches[1].group()))

    return total, product

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
data = [line.split()[0] for line in sys.stdin.readlines()]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1, sol2 = solve()

# # Log execution time
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
