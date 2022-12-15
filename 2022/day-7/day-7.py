import sys

class Node(object):
    def __init__(self, name, parent=None, size=None):
        self.name = name
        self.parent = parent
        self.size = size
        self.children = []

    # Add dir or file to level
    def add_child(self, node):
        self.children.append(node)

    # Get node with matching name from children
    def get(self, key):
        return next((x for x in self.children if x.name == key), None)

    # Get recursive sum for all files in level, including dirs
    def get_total_sum(self):
        sum = 0
        for node in self.children:
            if node.size != None:
                sum += node.size
            else:
                sum += node.get_total_sum()
        return sum

    # Get children
    def nodes(self):
        return self.children

    # Get all node names
    def keys(self):
        keys = []
        for node in self.children:
            keys.append(node.name)
        return keys

    # Print tree for debugging
    def print_tree(self, count=0):
        if count == 0:
            print("Name: " + self.name)
        if self.size != None:
            print(("-" * count) + "Size: " + str(self.size))
        else:
            for node in self.children:
                print(("-" * count) + "Child: " + node.name)
                node.print_tree(count + 2)

    # Formatted print
    def __str__(self):
        return "name = %s, parent = %s, size = %s, children = %s" % (self.name, "None" if self.parent == None else self.parent.name, "None" if self.size == None else self.size, self.children)

    # Just the node name
    def __repr__(self):
        return self.name

# Parse commands
data = [line.rstrip() for line in sys.stdin.readlines()]

# Create filesystem root "/"
fs = Node("/", None)

# Track cd commands for easy access in tree
path = [fs]
currentDir = path[0]

# Skip first "/" command and execute commands
for line in data[1:]:
    if line.startswith("$ ls"):
        continue
    elif line.startswith("$ cd"):
        loc = line.split("$ cd ")[1]
        if loc != "..":
            if loc not in currentDir.keys():
                currentDir.add_child(Node(loc, currentDir))
            path.append(currentDir.get(loc))
            currentDir = currentDir.get(loc)
        else:
            path.pop(len(path) - 1)
            currentDir = path[len(path) - 1]
    elif line.startswith("dir"):
        dir = line.split("dir ")[1]
        currentDir.add_child(Node(dir, currentDir))
    else:
        size = int(line.split()[0])
        name = line.split()[1]
        currentDir.add_child(Node(name, currentDir, size))

# Print tree for debugging
# fs.print_tree()

# Get recursive sum of nodes for solution 1 where <= 100000
def getSum(nodes):
    total = 0
    for node in nodes:
        # print(node)
        total += node.get_total_sum() if node.get_total_sum() <= 100000 else 0
        if len(node.nodes()) > 0:
            total += getSum(node.nodes())
    return total

# Params for solution 2
totalSpace = 70000000
reqSpace = 30000000
usedSpace = fs.get_total_sum()
unusedSpace = totalSpace - usedSpace
minToDelete = reqSpace - unusedSpace

# Track min dir size required to delete based on min diff seen
minSum = None
minDiff = None

# Initialize based on "/" first
if fs.get_total_sum() > minToDelete:
    minSum = fs.get_total_sum()
    minDiff = minSum - minToDelete

# Inspect directories until min diff found, update global vars with result
def inspectDir(nodes):
    global minSum, minDiff
    for node in nodes:
        if len(node.nodes()) > 0:
            sum = node.get_total_sum()
            diff = sum - minToDelete
            if sum > minToDelete and diff < minDiff:
                minSum = sum
                minDiff = diff
            inspectDir(node.nodes())

# Populate min sum from tree
inspectDir(fs.nodes())

# Solution 1 gets the recursive total sum where dirs are <= 100000
sol1 = getSum(fs.nodes())
# Solution 2 uses the tracked dir size with the min diff > reqSpace (30000000)
sol2 = minSum

print("Part 1: " + str(sol1))
print("Part 2: " + str(sol2))
