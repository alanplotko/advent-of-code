import sys, re, copy

# Parse data
data = [re.sub(r'[^\w\s]', '', x) for x in [line.rstrip() for line in sys.stdin.readlines()]]
numStacks = len(data[data.index('') - 1].split())
instructions = [x.split() for x in data[data.index('') + 1:]]

# Read lines and format as stacks
lines = [x.split() for x in [x[0].replace("    ", " - ") for x in [x.split(r'(\s+)') for x in data[0:data.index('') - 1]]]]
stacks = [[x for x in [x[i] if len(x) > i else '-' for x in lines] if x != "-"] for i in range(numStacks)]

print(data)
print(lines)
print(stacks)

# Perform the moves from the instructions
def executeInstructions(stack, needsReverse):
    # Deepcopy since we have a list of lists
    lst = copy.deepcopy(stack)
    for step in instructions:
        qty = int(step[1])
        srcPos = int(step[3]) - 1
        dstPos = int(step[5]) - 1
        # Select the first number of iems off the stack[src]
        selected = lst[srcPos][0:qty]
        # Reverse if picking off 1 item at a time rather than the full stack
        if needsReverse:
            selected.reverse()
        # Delete the selected items from src
        del lst[srcPos][0:qty]
        # Complete the move to dst (prepend)
        lst[dstPos] = selected + lst[dstPos]
    return lst

# Get the first item from each stack
sol1 = ''.join([x[0] for x in executeInstructions(stacks, True)])
sol2 = ''.join([x[0] for x in executeInstructions(stacks, False)])

print("Part 1: " + str(sol1))
print("Part 2: " + str(sol2))
