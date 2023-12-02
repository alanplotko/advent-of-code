import sys, time, re, math

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
prob1_mapping = {'red': 12, 'green': 13, 'blue': 14}

def parse_games(games):
    data = {}
    for game_id, game in enumerate(games):
        data[game_id + 1] = []
        for rounds in game:
            cubes = rounds.split(", ")
            round_data = {}
            for cube_count in cubes:
                count, color = cube_count.split(" ")
                round_data[color] = count
            data[game_id + 1].append(round_data)
    return data

# Check if game is valid for prob 1
def prob1_is_game_valid(game):
    for rounds in game:
        for color, count in rounds.items():
            if int(count) > prob1_mapping[color]:
                return False
    return True

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve1():
    total = 0
    for game_id, game in data.items():
        if not prob1_is_game_valid(game):
            continue
        else:
            total += game_id
    return total

def solve2():
    total = 0
    for game in data.values():
        min_cubes = {'red': 0, 'green': 0, 'blue': 0}
        for rounds in game:
            for color, count in rounds.items():
                min_cubes[color] = max(min_cubes[color], int(count))
        total += math.prod(min_cubes.values())
    return total

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
data = parse_games([line.split(":")[1].strip().split("; ") for line in sys.stdin.readlines()])

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1 = solve1()
sol2 = solve2()

# Log execution time
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
