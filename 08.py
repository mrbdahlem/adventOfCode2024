from collections import defaultdict
from types import SimpleNamespace
import helper
from datetime import datetime

def parse(data):
    parsed = SimpleNamespace()
    lines = data.splitlines()
    parsed.map = [list(line) for line in lines]

    # create a dictionary of all the frequencies and their locations
    antenna = defaultdict(list)
    for r in range(0, len(parsed.map)):
        for c in range(0, len(parsed.map[r])):
            if parsed.map[r][c] != ".":
                antenna[parsed.map[r][c]].append((c, r))

    # find the bounds of the map
    parsed.maxY = len(parsed.map) - 1
    parsed.maxX = len(parsed.map[0]) - 1

    parsed.antenna = antenna
    return parsed

################################
def printMap(map, an):
    for r in range(0, len(map)):
        for c in range(0, len(map[r])):
            if (c, r) in an:
                print("X", end="")
            else:
                print(map[r][c], end="")
        print()

def part1(data):
    # Solve the first part
    antinodes = set()

    # for each frequency, find the antinodes
    for freq in data.antenna.keys():
        # match each pair of antennas
        for i in range(len(data.antenna[freq])):
            for j in range(i + 1, len(data.antenna[freq])):
                loc1 = data.antenna[freq][i]
                loc2 = data.antenna[freq][j]

                # find the dx and dy between the two antennas
                dx = loc2[0] - loc1[0]
                dy = loc2[1] - loc1[1]

                # find the two antinodes that are on the line between the two antennas,
                # and are 2x the distance from one antenna as from the other
                pos1 = (loc2[0] + dx, loc2[1] + dy)
                pos2 = (loc1[0] - dx, loc1[1] - dy)       

                # add the antinodes to the set if they are within the bounds of the map
                if pos1[0] >= 0 and pos1[0] <= data.maxX and pos1[1] >= 0 and pos1[1] <= data.maxY:
                    antinodes.add(pos1)
                if pos2[0] >= 0 and pos2[0] <= data.maxX and pos2[1] >= 0 and pos2[1] <= data.maxY:
                    antinodes.add(pos2)

    return len(antinodes)

################################

def part2(data):
    antinodes = set()

    # for each frequency, find the antinodes along the line formed by each pair of antennas
    for freq in data.antenna.keys():
        for i in range(len(data.antenna[freq])):
            for j in range(i + 1, len(data.antenna[freq])):
                loc1 = data.antenna[freq][i]
                loc2 = data.antenna[freq][j]

                dx = loc2[0] - loc1[0]
                dy = loc2[1] - loc1[1]

                if (dx == 0):
                    # if the line is vertical, add all the antinodes along the line
                    for y in range(0, data.maxY + 1):
                        pos = (loc1[0], y)
                        antinodes.add(pos)
                else:
                    # if the line is not vertical, find the antinode at each x value where the y value is an integer
                    # point on the map
                    for x in range(0, data.maxX + 1):
                        # find the y value of the antinode at this x value
                        y = (dy * (x - loc1[0])) / dx + loc1[1]

                        # if the y value is an integer and within the bounds of the map, add the antinode
                        if y.is_integer() and y >= 0 and y <= data.maxY:
                            pos = (x, int(y))
                            antinodes.add(pos)
    return len(antinodes)

################################

def run(data):
    """
    Run both parts of the day
    """
    tstart = datetime.now()
    parsed = parse(data)
    print("------------------------")
    tparsed = datetime.now()
    
    # Solve the first part
    print("Part 1: ", part1(parsed))
    tp1 = datetime.now()

    # Solve the second part
    print("Part 2: ", part2(parsed))
    tp2 = datetime.now()

    print("------------------------")
    parseTime = (tparsed - tstart).total_seconds() * 1000
    part1Time = (tp1 - tparsed).total_seconds() * 1000
    part2Time = (tp2 - tp1).total_seconds() * 1000
    print(f"Parse Time: {parseTime:,.03f} ms")
    print(f"Part 1 Time: {part1Time:,.03f} ms")
    print(f"Part 2 Time: {part2Time:,.03f} ms")

################################

day = int(__file__.split("\\")[-1].split("/")[-1].split(".")[0])
print ("Day", day)

# load a sample data file for this day, if it exists
if helper.exists(f"{day:02}-samp"):
    samp = helper.load_data(f"{day:02}-samp")
else:
    samp = None

# load the actual data for this day
data = helper.load_data(day)

if samp:
    print("--------------- Sample Data ---------------")
    run(samp)
print("-------------------------------------------")
run(data)