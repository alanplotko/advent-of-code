import sys; data = sorted([sum(map(int, x.split(','))) for x in ((','.join([line.rstrip() for line in sys.stdin.readlines()])).split(',,'))],reverse=True); print("Part 1 = %d\nPart 2 = %d" % (data[0], sum(data[:3])))
