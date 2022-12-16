import sys, time

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    '''
    Inner function helpers
    '''
    def addx(val):
        nonlocal register, states
        states += [register, register + val]
        register += val

    def noop():
        nonlocal register, states
        states.append(register)

    '''
    Solution 1
    '''
    # Register starts at 1
    register = 1
    states = []

    # Run commands
    [addx(int(x[1])) if x[0] == "addx" else noop() for x in data]

    # Calculate signal strength by multiplying cycle (i) and register value
    # during cycle. Offset states index by 2 to get the register value during
    # the cycle instead of the end of the cycle.
    signalStrength = sum([i * states[i - 2] for i in range(20, 221, 40)])

    '''
    Solution 2
    '''
    # Image contains 6 rows of 40 width to display 8 capital letters for solution 2
    image = []
    currentRow = ""
    # To work during the cycle, prepend the first state to the beginning of the array
    states = [states[0]] + states
    for idx, state in enumerate(states):
        if len(currentRow) == 40:
            image.append(currentRow)
            currentRow = ""
        currentRow += ("#" if ((idx + 1) % 40) - state in [0, 1, 2] else ".")

    return (signalStrength, image)

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
data = [x.split() for x in [line.rstrip() for line in sys.stdin.readlines()]]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
signalStrength, image = solve()
sol1 = signalStrength
sol2 = [''.join(row) for row in image]

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")

# Print image for solution 2
print(f"Part 2:")
print(*sol2, sep='\n')
