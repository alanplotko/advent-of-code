import sys, time

'''''''''''''''''''''
MAIN SOLVER FUNCTION
'''''''''''''''''''''
def solve(decryptionKey=1, shuffleTimes=1):
    # Multiply every number by the decryption key, default to key = 1 for solution 1, since no key in use
    decryptedList = [x * decryptionKey for x in data]

    # This is the copy of the list we will work with that tracks indices, since there are duplicates
    toShuffle = [(i, x) for i, x in enumerate(decryptedList)]

    # Shuffle once for solution 1, and 10 times for solution 2
    for i in range(shuffleTimes):
        for idx, d in enumerate(decryptedList):
            # Find the number in question with the original index (idx)
            searchKey = (idx, d)

            # Get its position in the shuffled array and slice it out
            index = toShuffle.index(searchKey)
            slicedList = toShuffle[:index] + toShuffle[index + 1:]

            # Loop around the list if out of bounds
            newIndex = (index + d) % len(slicedList)

            if DEBUG:
                print(f"{d} moves {d} from {idx} to {newIndex}")

            # If new index is at 0 or end of list, we'll want to append/prepend accordingly.
            # This is one of the properties described in the question where it kind of skips
            # by 1. Otherwise, we can insert at the index as is.
            if newIndex == 0:
                slicedList.append(searchKey)
            elif newIndex == len(slicedList):
                slicedList.prepend(searchKey)
            else:
                slicedList.insert(newIndex, searchKey)
            toShuffle = slicedList

            if DEBUG:
                print(f"{toShuffle}\n")

    # Get the location of the 0 to anchor against
    anchor = [x[1] for x in toShuffle].index(0)

    # Get sum of values at provided positions 1000, 2000, and 3000 (hardcoded).
    # Must start at index for value 0 and loop around if out of bounds.
    return sum([toShuffle[(anchor + i) % len(toShuffle)][1] for i in [1000, 2000, 3000]])

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
data = [int(x) for x in [line.rstrip() for line in sys.stdin.readlines()]]

'''''''''''''''''''''
SOLVING & LOGGING
'''''''''''''''''''''
sol1 = solve()
sol2 = solve(811589153, 10)

# Log execution time and solutions
print(f"--- Ran for {(time.time() - startTime)} seconds ---")
print(f"Part 1: {str(sol1)}")
print(f"Part 2: {str(sol2)}")
