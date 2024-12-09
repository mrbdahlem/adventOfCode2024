from math import sqrt
from collections import defaultdict
import helper
from datetime import datetime

day = int(__file__.split("\\")[-1].split("/")[-1].split(".")[0])
print ("Day", day)

tstart = datetime.now()

# load the data for this day (or a sample file)
data = helper.load_data(day)
# data = helper.load_data(f"{day:02}-samp")

# break each line down into characters to form the map
lines = data.splitlines()
map = [list(line) for line in lines]

# create a dictionary of all the frequencies and their locations
antenna = defaultdict(list)
for r in range(0, len(map)):
    for c in range(0, len(map[r])):
        if map[r][c] != ".":
            antenna[map[r][c]].append((c, r))

# find the bounds of the map
maxY = len(map) - 1
maxX = len(map[0]) - 1

print("------------------------")
tparsed = datetime.now()

def printMap(map, an):
    for r in range(0, len(map)):
        for c in range(0, len(map[r])):
            if (c, r) in an:
                print("X", end="")
            else:
                print(map[r][c], end="")
        print()

# Solve the first part
antinodes = set()

# for each frequency, find the antinodes
for freq in antenna.keys():
    # match each pair of antennas
    for i in range(len(antenna[freq])):
        for j in range(i + 1, len(antenna[freq])):
            loc1 = antenna[freq][i]
            loc2 = antenna[freq][j]

            # find the dx and dy between the two antennas
            dx = loc2[0] - loc1[0]
            dy = loc2[1] - loc1[1]

            # find the two antinodes that are on the line between the two antennas,
            # and are 2x the distance from one antenna as from the other
            pos1 = (loc2[0] + dx, loc2[1] + dy)
            pos2 = (loc1[0] - dx, loc1[1] - dy)       

            # add the antinodes to the set if they are within the bounds of the map
            if pos1[0] >= 0 and pos1[0] <= maxX and pos1[1] >= 0 and pos1[1] <= maxY:
                antinodes.add(pos1)
            if pos2[0] >= 0 and pos2[0] <= maxX and pos2[1] >= 0 and pos2[1] <= maxY:
                antinodes.add(pos2)
            


print("Part 1: ", len(antinodes))

tp1 = datetime.now()

# Solve the second part
ans2 = 0
antinodes = set()

# for each frequency, find the antinodes along the line formed by each pair of antennas
for freq in antenna.keys():
    for i in range(len(antenna[freq])):
        for j in range(i + 1, len(antenna[freq])):
            loc1 = antenna[freq][i]
            loc2 = antenna[freq][j]

            dx = loc2[0] - loc1[0]
            dy = loc2[1] - loc1[1]

            if (dx == 0):
                # if the line is vertical, add all the antinodes along the line
                for y in range(0, len(map)):
                    pos = (loc1[0], y)
                    antinodes.add(pos1)
            else:
                # if the line is not vertical, find the antinode at each x value where the y value is an integer
                # point on the map
                for x in range(0, len(map[0])):
                    # find the y value of the antinode at this x value
                    y = (dy * (x - loc1[0])) / dx + loc1[1]

                    # if the y value is an integer and within the bounds of the map, add the antinode
                    if y.is_integer() and y >= 0 and y <= maxY:
                        pos = (x, int(y))
                        antinodes.add(pos)

print("Part 2: ", len(antinodes), '1291 - low')

tp2 = datetime.now()

print("------------------------")
print(f"Parse Time: {((tparsed - tstart).total_seconds() * 1000):.3f} ms")
print(f"Part 1 Time: {(tp1 - tparsed).total_seconds() * 1000:.3f} ms")
print(f"Part 2 Time: {(tp2 - tp1).total_seconds() * 1000:.3f} ms")