import sys

def getPriority(letter):
    return ord(letter) - 38 if letter.isupper() else ord(letter) - 96

def findCommon(arr):
    return ''.join(set.intersection(*map(set, arr)))

# Parse data
data = [line.rstrip() for line in sys.stdin.readlines()]

# Part 1, split each line in half
part1 = [[x[:len(x)//2], x[len(x)//2:]] for x in data]
sol1 = sum(list(map(getPriority, [findCommon(x) for x in part1])))

# Part 2, read 3 lines at a time
part2 = [x for x in (data[i:i + 3] for i in range(0, len(data), 3))]
sol2 = sum(list(map(getPriority, [findCommon(x) for x in part2])))

print("Part 1: " + str(sol1))
print("Part 2: " + str(sol2))
