from types import SimpleNamespace
import helper
from datetime import datetime

def parse(data):
    parsed = SimpleNamespace()

    # turn the data into a 2d array of integers, the heightmap
    lines = data.strip().split("\n")
    parsed.map = [[int(x) for x in list(l)] for l in lines]
    
    # find all the trailheads in the map
    parsed.trailheads = set()
    for r in range(len(parsed.map)):
        for c in range(len(parsed.map[r])):
            if parsed.map[r][c] == 0:
                parsed.trailheads.add((r, c))

    return parsed

################################

def part1(data):
    """
    Find the total of the number of highest points reachable from each trailhead
    """
    count = 0
    for th in data.trailheads:
        # each trailhead is a starting point for a search for majestic points (the highest points)
        majesty = set()
        findMajesticPoints(data.map, th, majesty)
        count += len(majesty)

    return count

def findMajesticPoints(map, point, majesty):
    """ 
    Recursively find all of the "majestic" points reachable from the given point (points with a height of 9)
    """

    # Find the height of the current point
    height = map[point[0]][point[1]]

    # If the height is 9, add it to the set of majestic points
    if height == 9:
        majesty.add(point)
        return

    # Otherwise, check the surrounding points to see if they are a valid trail leading up one level
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        r = point[0] + dr
        c = point[1] + dc

        # If the point is within the bounds of the map and is the next level up, recursively search
        # from that point
        if r >= 0 and r < len(map) and c >= 0 and c < len(map[r]):
            if map[r][c] == height + 1:
                findMajesticPoints(map, (r, c), majesty)

################################

def part2(data):
    """
    Find the total number of trails that can be followed from each trailhead that lead to a point
    with a height of 9
    """
    count = 0
    for th in data.trailheads:
        count += countTrails(data, th)

    return count

def countTrails(data, point):
    """
    Count the number of trails that can be followed from the given point that lead to a point 
    with a height of 9
    """

    # Find the height of the current point
    height = data.map[point[0]][point[1]]

    # If the height is 9, we have a trail that leads to a height of 9
    if height == 9:
        return 1
    
    # Otherwise, check the surrounding points to see if they are a valid trail leading up one level
    count = 0
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        r = point[0] + dr
        c = point[1] + dc

        # If the next point is within the bounds of the map and is the next level up, recursively search
        # from that point
        if r >= 0 and r < len(data.map) and c >= 0 and c < len(data.map[r]):
            if data.map[r][c] == height + 1:
                count += countTrails(data, (r, c))

    return count

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