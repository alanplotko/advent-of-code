import sys

data = [x.split() for x in [line.rstrip() for line in sys.stdin.readlines()]]

# Solution 1
def addx(val):
    global register, states
    states += [register, register + val]
    register += val

def noop():
    global register, states
    states.append(register)

register = 1
states = []
[addx(int(x[1])) if x[0] == "addx" else noop() for x in data]
signalStrength = sum([i * states[i - 2] for i in range(20, 221, 40)])

# Solution 2
currentRow = ""
states = [states[0]] + states
for idx, state in enumerate(states):
    if len(currentRow) == 40:
        print(currentRow)
        currentRow = ""
    currentRow += ("#" if ((idx + 1) % 40) - state in [0, 1, 2] else ".")

sol1 = signalStrength
sol2 = "See 8 capital letters in rendered image above"

print("Part 1: " + str(sol1))
print("Part 2: " + str(sol2))
