import sys, time

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# Move first head and then simulate for every following head (tail)
def move(numKnots, axis, direction, movement, heads, tails):
    # For every movemet, we start with the head
    for x in range(movement):
        # X or Y move +1 (right, up) or -1 (left, down)
        heads[0][axis] += direction
        # We then work our way down the knots
        for i in range(numKnots - 1):
            head = heads[i] # Current position is head
            tail = heads[i + 1] # Next position is the adjacent tail for this head

            # Check for diagonal, match head X coordinate
            if abs(head[0] - tail[0]) == 1 and abs(head[1] - tail[1]) == 2:
                # Align to same X pos, then move up or down 1
                tail[0] = head[0]
                if head[1] > tail[1]:
                    tail[1] += 1
                else:
                    tail[1] -= 1

                if DEBUG:
                    print("Movement: %s, %s" % (head, tail))

                # Track tail movement if on last head (tail of Snake)
                if i == numKnots - 2:
                    tails.add(tuple(heads[-1].copy()))
                continue
            # Check for diagonal, match head Y coordinate
            elif abs(head[1] - tail[1]) == 1 and abs(head[0] - tail[0]) == 2:
                # Align to same Y pos, then move left or right 1
                tail[1] = head[1]
                if head[0] > tail[0]:
                    tail[0] += 1
                else:
                    tail[0] -= 1
                if DEBUG:
                    print("Movement: %s, %s" % (head, tail))

                # Track tail movement if on last head (tail of Snake)
                if i == numKnots - 2:
                    tails.add(tuple(heads[-1].copy()))
                continue
            # X
            if head[0] - tail[0] == 2:
                tail[0] += 1
            elif head[0] - tail[0] == -2:
                tail[0] -= 1
            # Y
            if head[1] - tail[1] == 2:
                tail[1] += 1
            elif head[1] - tail[1] == -2:
                tail[1] -= 1

            # Track tail movement if on last head (tail of Snake)
            if i == numKnots - 2:
                tails.add(tuple(heads[-1].copy()))

            if DEBUG:
                print("Movement: %s, %s" % (head, tail))

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
# Solve for number of knots, track last head (tail)
def solve(numKnots):
    # Number of knots, last head is the tail, think of it like Snake
    heads = [[0, 0] for x in range(numKnots)]
    tails = set()

    # For each command, we move the head and then propagate down the snake
    for command in data:
        if command[0] == 'L':
            # X (0) moves left (-1)
            move(numKnots, 0, -1, command[1], heads, tails)
        elif command[0] == 'R':
            # X (0) moves right (+1)
            move(numKnots, 0, 1, command[1], heads, tails)
        elif command[0] == 'U':
            # Y (1) moves up (+1)
            move(numKnots, 1, 1, command[1], heads, tails)
        elif command[0] == 'D':
            # Y (1) moves down (-1)
            move(numKnots, 1, -1, command[1], heads, tails)
        else:
            continue

        if DEBUG:
            print("%s, %s" % (command, heads))

    return len(tails)

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
data = [[x.split()[0], int(x.split()[1])] for x in [line.rstrip() for line in sys.stdin.readlines()]]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
# Solve for number of knots
sol1 = solve(2)
sol2 = solve(10)

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
