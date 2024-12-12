from types import SimpleNamespace
import helper
from datetime import datetime

from collections import defaultdict
import re
from functools import cache

def parse(data):
    parsed = SimpleNamespace()
    lines = data.strip().split("\n")

    # parse the data into a 2D array and store the width and height
    parsed.map = [list(x) for x in lines]
    parsed.width = len(parsed.map[0])
    parsed.height = len(parsed.map)

    return parsed

################################

def area(region):
    """
    Calculate the area of a region
    """
    return len(region)

def perimeter(region):
    """
    Find the sections of fence that would bound the region
    """
    perimeter = []
    for x, y in region:
        if (x-1, y) not in region:
            perimeter.append((x*2, y*2, x*2, y*2+2, 'l'))
        if (x+1, y) not in region:
            perimeter.append((x*2+2, y*2, x*2+2, y*2+2, 'r'))
        if (x, y-1) not in region:
            perimeter.append((x*2, y*2, x*2+2, y*2, 't'))
        if (x, y+1) not in region:
            perimeter.append((x*2, y*2+2, x*2+2, y*2+2, 'b'))
    return perimeter

def part1(data):
    """
    Calculate the total cost to fence in all the regions at full price based on the perimeter 
    and area of the regions
    """
    map = data.map
    w = data.width
    h = data.height

    visited = set() # set of visited coordinates when traversing the map to build regions

    def findNextRegion():
        """
        Find the next unvisited coordinate in the map to start building a region
        """
        for y in range(h):
            for x in range(w):
                if (x, y) not in visited:
                    return (x, y)
        return None
    
    def findNeighbors(x, y):
        """
        Find the neighbors of a plot that are part of the same region as the plot
        """
        neighbors = []
        if x > 0 and map[y][x-1] == map[y][x]:
            neighbors.append((x-1, y))
        if x < w-1 and map[y][x+1] == map[y][x]:
            neighbors.append((x+1, y))
        if y > 0 and map[y-1][x] == map[y][x]:
            neighbors.append((x, y-1))
        if y < h-1 and map[y+1][x] == map[y][x]:
            neighbors.append((x, y+1))
        return neighbors
    
    def mapRegion(x, y, region):
        """
        Recursively map out the region starting at the given plot
        """
        visited.add((x, y))
        region.add((x, y))

        neighbors = findNeighbors(x, y)
        for n in neighbors:
            if n not in visited:
                mapRegion(n[0], n[1], region)

        return region
    
    # Map out all the regions in the map
    regions = []
    nextRegion = findNextRegion()
    while nextRegion:
        region = set()
        regions.append((mapRegion(nextRegion[0], nextRegion[1], region), 
                       perimeter(region)))
        nextRegion = findNextRegion()

    data.regions = regions

    # Calculate the total cost to fence in all the regions
    total = 0
    for region, fence in regions:
        total += area(region) * len(fence)

    return total

################################
def findNextSection(x, y, fence):
    """
    Find the next section of fence to walk along
    """
    for f in fence:
        # find the next section of fence that has an endpoint at the given location
        if (f[0], f[1]) == (x, y):
            fence.remove(f)
            return f, f[2], f[3], f[4]
        if (f[2], f[3]) == (x, y):
            fence.remove(f)
            return f, f[0], f[1], f[4]
        
    # if no section of fence was found, return Nones
    return None, None, None, None

def walkPerimeters(sections):
    """
    Walk the perimeters of the regions to calculate the number of turns 
    (and thus the number of sides of the region)
    """
    turns = 0
    # start at the first section of fence
    section = sections.pop(0)
    odir = dir = section[4]
    x, y = section[2], section[3]

    # If there are more sections of fence to walk along (or we haven't finished the last one)
    while sections or section:
        # find the next section of fence we will need to walk along
        section, x, y, nextDir = findNextSection(x, y, sections)

        # if no section was found, we've reached the end of the region
        if section is None:
            # if the direction is not the same as the original direction for this region's
            # fence, we ended at a turn and need to count it
            if odir != dir:
                turns += 1
                
            # if there are more sections of fence to walk along,
            # prepare to start walking along the next one
            if sections:
                section = sections.pop(0)
                x, y = section[2], section[3]
                odir = dir = section[4]

        # if the next section of fence is in a different direction, we've reached a turn
        elif dir != nextDir:
            turns += 1
            dir = nextDir

    # print (turns, fences)
    return turns

def part2(data):
    """
    Calculate the total cost to fence in all the regions, but this time use the discounted
    cost of the regions based on the region area an number of sides it has rather than its
    perimeter
    """
    total = 0
    for region, fences in data.regions:
        sides = walkPerimeters(fences)
        total += sides * area(region)

    return total

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
    print("Part 1: ", part1(parsed), "1522850")
    tp1 = datetime.now()

    # Solve the second part
    print("Part 2: ", part2(parsed), "953738")
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
# exit()
print("-------------------------------------------")
run(data)