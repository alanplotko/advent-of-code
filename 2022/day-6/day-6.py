import sys

# Parse stream as string
data = [line.rstrip() for line in sys.stdin.readlines()][0]

# Work in sliced chunks of the string, checking if the set matches the marker length to work with
def getEndPosition(data, markerLength):
    # Start position is first character (0) to last character that can fit the marker length
    for idx in range(0, len(data) - markerLength - 1):
        # If any character is deduped from set, then it's not all unique and < marker length
        if len(set([*data[idx:idx + markerLength]])) == markerLength:
            # We want the end position (start position + marker length)
            return idx + markerLength

# Get end position for string with marker length of 4 and 14
sol1 = getEndPosition(data, 4)
sol2 = getEndPosition(data, 14)

print("Part 1: " + str(sol1))
print("Part 2: " + str(sol2))
