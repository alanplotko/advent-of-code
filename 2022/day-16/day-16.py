import sys, time, re
from collections import defaultdict

'''''''''''''''''''''
Graph and Dijsktra implementation
From https://benalexkeen.com/implementing-djikstras-shortest-path-algorithm-with-python/
'''''''''''''''''''''
class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# Breadth-first search
def findMaxFlow(currentValve, minutes, visited, valvesToCheck):
    # Add current valve to visited set
    visited = visited | {currentValve}

    # Only look at key valves (> 0 pressure) we haven't yet visited
    valvesToCheck = valvesToCheck - visited

    maxFlow = 0
    for targetValve in valvesToCheck:
        # Minutes spent include the distance to travel to the key valve and the 1 minute to open it
        remainingTime = minutes - distances[(currentValve, targetValve)]['dist'] - 1

        # If we have enough time left, keep going
        if remainingTime > 0:
            flow = valves[targetValve]['flow'] * remainingTime
            flow += findMaxFlow(targetValve, remainingTime, visited, valvesToCheck)
            maxFlow = max(flow, maxFlow)
    return maxFlow

# Breadth-first search, but also track the combinations as we go alongs
def findAllFlowCombinations(currentValve, currentFlow, minutes, visited, controlSet, valvesToCheck):
    # Add current valve to visited set
    visited = visited | {currentValve}

    # Only look at key valves (> 0 pressure) we haven't yet visited
    valvesToCheck = valvesToCheck - visited

    maxFlow = 0

    # Build up all combinations of valves and their best achievable total pressure
    key = frozenset(visited - {"AA"})
    if key in controlSet:
        controlSet[key] = max(controlSet[key], currentFlow)
    else:
        controlSet[key] = currentFlow

    for targetValve in valvesToCheck:
        if currentValve != targetValve:
            # Minutes spent include the distance to travel to the key valve and the 1 minute to open it
            remainingTime = minutes - distances[(currentValve, targetValve)]['dist'] - 1

            # If we have enough time left, keep going
            if remainingTime > 0:
                flow = valves[targetValve]['flow'] * remainingTime
                newFlow, controlSet = findAllFlowCombinations(targetValve, flow + currentFlow, remainingTime, visited, controlSet, valvesToCheck)
                maxFlow = max(flow + newFlow, maxFlow)
    return (maxFlow, controlSet)

# For every path we've precomputed in findAllFlowCombinations(...), we need
# to find the complement (missing set of key valves)
def findComplementForControlSet(controlSet, currentValve):
    if currentValve not in controlSet:
        maxFlow = 0
        for targetValve in currentValve:
            nextSetToCheck = currentValve - {targetValve}
            newFlow = findComplementForControlSet(controlSet, nextSetToCheck)
            maxFlow = max(newFlow, maxFlow)
        controlSet[currentValve] = maxFlow
    return controlSet[currentValve]

# With the combinations precomputed in findComplementForControlSet(),
# assign 1 path to the human and the other to the elephant. Add the associated
# flows together to get the total flow achieved by both.
def computeMaxFlowForTwo(controlSet):
    maxFlow = 0
    for humanPath in controlSet:
        # Elephant path = complement of human path
        elephantPath = frozenset(keyValves - {start} - humanPath)
        # Whatever valves the human opens, the elephant opens the complement,
        # or in other words, the other remaining key valves
        totalFlow = controlSet[humanPath] + controlSet[elephantPath]
        maxFlow = max(totalFlow, maxFlow)
    return maxFlow

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    # Get max flow for 30 minutes, control set not needed
    flowSol1 = findMaxFlow(start, 30, set(), keyValves)

    controlSet = findAllFlowCombinations(start, 0, 26, set(), {}, keyValves)[1]

    # For every valve combination and respective flow, find remaining key
    # valves to be completed by the elephant
    valvesToCheck = frozenset(keyValves - {start})
    findComplementForControlSet(controlSet, valvesToCheck)

    # Get max flow when considering every combination of valves opened
    # by human vs. elephant
    flowSol2 = computeMaxFlowForTwo(controlSet)

    if TRACE:
        for key in controlSet.keys():
            print(f"{key}: {controlSet[key]}")

    return (flowSol1, flowSol2)

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
data = [line.rstrip() for line in sys.stdin.readlines()]
matches = [re.findall(r'^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*?)$', line) for line in data]
valves = {}
for match in matches:
    valves[match[0][0]] = { 'key': match[0][0], 'flow': int(match[0][1]), 'next': match[0][2].split(', ') }

# Print set of valves parsed from input
if DEBUG:
    for key in valves.keys():
        print(f"{key}: {valves[key]}")
    print() # Newline

# Construct graph from valves dict to derive shortest paths between key
# valves (> 0 pressure) using Djikstra
graph = Graph()
for key in valves.keys():
    for node in valves[key]['next']:
        graph.add_edge(key, node, 1)

# Always start at valve key = AA
start = 'AA'

# Valves with > 0 pressure + starting  valve
keyValves = {x for x in valves.keys() if valves[x]['flow'] > 0 or x == start}

# Precompute all distances between key valves and starting valve
distances = {}
for src in keyValves:
    for dst in keyValves:
        # Ignore disance from valve to self
        if src != dst:
            path = dijsktra(graph, src, dst)
            # Don't count starting node in path
            distances[(src, dst)] = {
                'path': path,
                'dist': len(path) - 1
            }

# Print distances for debugging
if TRACE:
    for key in distances.keys():
        print(f"{key}: {distances[key]}")

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1, sol2 = solve()

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
