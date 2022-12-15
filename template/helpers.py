# Helper functions to get trees in row or column
def parseGrid(arr):
    return [list(map(int, x)) for x in [[*x] for x in arr]]

def top(arr, row, col):
    return [line[col] for line in arr[0:row]]

def bottom(arr, row, col):
    return [line[col] for line in arr[row+1:len(arr)]]

def left(arr, row, col):
    return arr[row][0:col]

def right(arr, row, col):
    return arr[row][col+1:len(arr)]

def topAdjacent(arr, row, col):
    return arr[row-1][col] if row - 1 >= 0 else None

def bottomAdjacent(arr, row, col):
    return arr[row+1][col] if row + 1 <= len(arr[row]) - 1 else None

def leftAdjacent(arr, row, col):
    return arr[row][col-1] if col - 1 >= 0 else None

def rightAdjacent(arr, row, col):
    return arr[row][col+1] if col + 1 <= len(arr[row]) - 1 else None

def getAllAdjacent(arr, row, col, showNone=True):
    adjacent = [
        topAdjacent(arr, row, col),
        bottomAdjacent(arr, row, col),
        leftAdjacent(arr, row, col),
        rightAdjacent(arr, row, col)
    ]
    return adjacent if showNone else [x for x in adjacent if x != None]

# Node class for n-ary tree
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
