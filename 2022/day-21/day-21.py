import sys, time, re, sympy
from operator import add, sub, mul, floordiv

'''''''''''''''''''''
HELPERS
'''''''''''''''''''''
# Use floor div to
ops = { "+": add, "-": sub, "*": mul, "/": floordiv }

def translateSol1(node):
    # We stop once we have a number
    if node.isdigit():
        return int(node)

    # Extract expression components
    lhs, action, rhs = node.split()

    # Recursively substitute and solve until we get our result
    return ops[action](translateSol1(data[lhs]), translateSol1(data[rhs]))

def translateSol2(node):
    # We stop once we have a number or x to solve for
    if node.isdigit() or node == 'x':
        return node

    # Extract expression components
    lhs, action, rhs = node.split()

    # Recursively substitute and solve until we get a left and right side
    left = translateSol2(data[lhs])
    right = translateSol2(data[rhs])

    # Insert parentheses to build up our final expression
    return f"({left} {action} {right})"

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve():
    # Solve for sol1 where we simply have to substitute until we have a integer solution
    sol1 = translateSol1(data['root'])

    # For solution 2, update root equation to "==" to split on later, and update integer at 'humn' to 'x'
    lhs, action, rhs = data['root'].split()
    data['root'] = f"{lhs} == {rhs}"
    data['humn'] = 'x'

    # Get both sides for new root
    left, right = translateSol2(data['root']).split(' == ')

    # Remove outer parentheses
    left = left[1:len(left)]
    right = right[0:len(right) - 1]

    # Simplify side without x to integer and move to the other side
    # Return int of eval result since eval will treat / as truediv
    simplified = f"{left} - {int(eval(right))}" if 'x' in left else f"{right} - {int(eval(left))}"

    # Solve for x in simplified = 0 using sympy
    x = sympy.Symbol('x')
    sol2 = sympy.solve(simplified, x)[0] # There's only 1 answer, so default to answer at index 0

    return sol1, sol2

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
data = {x.split(': ')[0]: x.split(': ')[1] for x in [line.rstrip() for line in sys.stdin.readlines()]}

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1, sol2 = solve()

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
