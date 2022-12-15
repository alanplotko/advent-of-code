import sys

# Parse data
data = [x.split() for x in [line.rstrip() for line in sys.stdin.readlines()]]

"""
Solution 1
"""

# Register starts at 1
register = 1
states = []
signalStrength = 0

# This gives the end result per cycle
for command in data:
    # Append regardless of noop or addx
    states.append(register)
    # Perform the addition only for addx
    if command[0] == 'addx':
        register += int(command[1])
        states.append(register)

# Cycles are: 20, 60, 100, 140, 180, 220
for i in range(20, 221, 40):
    # For debugging
    # print("State %d = %d, adding %d" % (i, states[i - 2], i * states[i - 2]))

    # Calculate signal strength by multiplying cycle (i) and register value
    # during cycle. Offset states index by 2 to get the register value during
    # the cycle instead of the end of the cycle.
    signalStrength += (i * states[i - 2])

"""
Solution 2
"""

# Image contains 6 rows of 40 width to display 8 capital letters for solution 2
image = []
# Track current row of 40 cycles in the image
currentRow = ""

# To work during the cycle, prepend the first state to the beginning of the array
states = [states[0]] + states
for idx, state in enumerate(states):
    # Start new row every 40 cycles
    if len(currentRow) == 40:
        image.append(currentRow)
        currentRow = ""

    # Always work from cycles 1-40
    cycle = (idx + 1) % 40

    # Check if within 0-2, since the sprite is 3 wide
    if cycle - state in [0, 1, 2]:
        currentRow += "#" # Matched sprite position
    else:
        currentRow += "." # Sprite was not in range

    # For debugging
    # print("Cycle #%d: %d" % (cycle if cycle != 0 else 40, state))
    # print(currentRow)

sol1 = signalStrength
sol2 = "See 8 capital letters in rendered image below"

print("Part 1: " + str(sol1))
print("Part 2: " + str(sol2))

for row in image:
    print(row)
