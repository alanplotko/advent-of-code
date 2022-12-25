import sys, time

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve(fuels):
    # Count total for all fuel reqs
    total = 0

    # Split fuel req into individual characters of [0-2], -, and =
    for req in fuels:
        digits = [*req][::-1]
        for place, digit in enumerate(digits):
            if digit == '-':
                parsed = -1
            elif digit == '=':
                parsed = -2
            else:
                parsed = int(digit)
            # Add to total the parsed digit's value * its place in 5s
            total += (parsed * pow(5, place))

    '''
    When n % 5 = 3, we add a = in SNAFU. When n % 5 = 4, we add a - in SNAFU.
    3 % 5 = 3, so we need a =. But we carry over a 1 in the process. That
    gives us 1= for 3 and 1- for 4.

    Decimal          SNAFU
        1              1
        2              2
        3             1=
        4             1-
        5             10
        6             11
        7             12
        8             2=
        9             2-
       10             20

    For 4890 from the test case:
    1) 4890 % 5 = 0. 4890 // 5 = 978.
    2) 978 % 5 = 3. 978 // 5 = 195 + 1 carried over = 196.
    3) 196 % 5 = 1. 196 // 5 = 39.
    4) 39 % 5 = 4. 39 // 5 = 7 + 1 carried over = 8.
    5) 8 % 5 = 3. 8 // 5 = 1 + 1 carried over = 2.
    6) 2 % 5 = 2. 2 // 5 = 0. We're done.

    In order, our mod results were:
    1) 0
    2) 3 -> =
    3) 1
    4) 4 -> -
    5) 3 -> =
    6) 2

    We need to reverse to get the proper order, so that's 2=-1=0 in reverse order.
    '''

    key = ""
    while total != 0:
        remainder = total % 5
        if remainder == 3:
            key += "="
        elif remainder == 4:
            key += "-"
        else:
            key += str(remainder)
        total = total // 5 + (1 if remainder >= 3 else 0)

    # Return key in reverse
    return key[::-1]

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

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1 = solve(data)

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: We have all 50 stars to start the blender! 50-star smoothie, here we come! We're done! :)")
