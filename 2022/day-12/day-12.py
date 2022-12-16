import sys, time
from collections import deque
from copy import deepcopy

'''''''''''''''''''''
Edited Djikstra implementation
From https://www.techiedelight.com/find-shortest-path-source-destination-matrix-satisfies-given-constraints/
'''''''''''''''''''''
# A queue node used in BFS
class Node:
	# (x, y) represents coordinates of a cell in the matrix
	# maintain a parent node for the printing path
	def __init__(self, x, y, parent=None):
		self.x = x
		self.y = y
		self.parent = parent

	def __repr__(self):
		return str((self.x, self.y))

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

# The function returns false if (x, y) is not a valid position
def isValid(x, y, rowSize, colSize):
	return (0 <= x < rowSize) and (0 <= y < colSize)


# Utility function to find path from source to destination
def getPath(node, path=[]):
	if node:
		getPath(node.parent, path)
		path.append(node)

# Find the shortest route in a matrix from source cell (x, y) to
# destination cell (N-1, N-1)
def findPath(matrix, start, end):
	# Set up vars
	x = start[0]
	y = start[1]
	a = end[0]
	b = end[1]

	# Below lists detail all four possible movements from a cell
	rowMovement = [-1, 0, 0, 1]
	colMovement = [0, -1, 1, 0]

	# base case
	if not matrix or not len(matrix):
		return

	rowSize = len(matrix)
	colSize = len(matrix[0])

	# create a queue and enqueue the first node
	q = deque()
	src = Node(x, y)
	q.append(src)

	# set to check if the matrix cell is visited before or not
	visited = set()

	key = (src.x, src.y)
	visited.add(key)

	# loop till queue is empty
	while q:
		# dequeue front node and process it
		curr = q.popleft()
		i = curr.x
		j = curr.y

		# return if the destination is found
		if i == a and j == b:
			path = []
			getPath(curr, path)
			return path

		# value of the current cell
		n = matrix[i][j]

		# check all four possible movements from the current cell
		# and recur for each valid movement
		for k in range(len(rowMovement)):
			# get next position coordinates using the value of the current cell
			x = i + rowMovement[k]
			y = j + colMovement[k]

			# check if it is possible to go to the next position
			# from the current position
			if isValid(x, y, rowSize, colSize) and matrix[x][y] - n <= 1:
				# print("(%d, %d) = %s -> (%d, %d) = %s with diff = %d" % (i, j, chr(n + 96), x, y, chr(matrix[x][y] + 96), matrix[x][y] - n))
				# construct the next cell node
				next = Node(x, y, curr)
				key = (next.x, next.y)
				# print("%s: %s" % (next, chr(matrix[x][y] + 96)))

				# if it isn't visited yet
				if key not in visited:
					# enqueue it and mark it as visited
					q.append(next)
					visited.add(key)

	# return None if the path is not possible
	return None

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# Translate letters to numbers
def translate(n):
	if n == 'S':
		return 1
	if n == 'E':
		return 26
	return ord(n) - 96

# Get start and end positions
def findPositions(startChar):
	global data, rows, cols
	start = []
	end = None
	for i in range(rows):
		for j in range(cols):
			if data[i][j] == startChar:
				start.append([i, j])
			if data[i][j] == 'E':
				end = [i, j]
	return (start, end)

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
# Solve for all starting positions, return minimum length
def solve(positions, filenamePrefix):
	letterMatrix = deepcopy(data)
	numberMatrix = deepcopy(matrix)
	startPositions = positions[0]
	end = positions[1]

	if DEBUG:
		print("Start = %s, end = %s" % (startPositions, end))

	paths = []
	for start in startPositions:
		path = findPath(numberMatrix, start, end)
		if path != None:
			paths.append(path)
	pathLengths = [len(path) - 1 for path in paths]
	minLength = min(pathLengths)
	pathIdx = pathLengths.index(minLength)
	minPath = paths[pathIdx]

	# Sketch out minimum path taken in uppercase and write to file for debugging
	for node in minPath:
		letterMatrix[node.x][node.y] = letterMatrix[node.x][node.y].upper()

	# Remove all unvisited points in lowercase
	for i in range(len(letterMatrix)):
		for j in range(len(letterMatrix[0])):
			if not letterMatrix[i][j].isupper():
				letterMatrix[i][j] = '.'

	# Write output to file
	if TRACE:
		f = open(filenamePrefix + "-output.txt", "w")
		for x in letterMatrix:
			f.write(''.join(x) + "\n")
		f.close()

	# Return minimum path length encountered
	return minLength

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
data = [[*x] for x in [line.rstrip() for line in sys.stdin.readlines()]]
rows = len(data)
cols = len(data[0])

# Convert data to number values
matrix = [list(map(lambda n: translate(n), x)) for x in data]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1 = solve(findPositions('S'), "sol1")
sol2 = solve(findPositions('a'), "sol2")

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
