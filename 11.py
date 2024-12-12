from types import SimpleNamespace
import helper
from datetime import datetime

from collections import defaultdict
import re
from functools import cache

def parse(data):
    parsed = SimpleNamespace()
    parsed.line = [int(x) for x in data.split(" ")]
    return parsed

################################

def part1(data):
    """
    Simulate the stone transformation for 25 iterations
    """

    orig = data.line

    for _ in range(25):
        # simulate the transformation of the stones, following the rules
        new = []
        for stone in orig:
            if stone == 0:
                # if the stone's inscription is 0, it transforms into 1
                new.append(1)
            elif len(str(stone)) % 2 == 0:
                # if the stone has an even number of digits, it splits in half
                name = str(stone)
                name1 = int(name[:len(name)//2])
                name2 = int(name[len(name)//2:])
                new.append(name1)
                new.append(name2)
            else:
                # otherwise, the stone's inscription is multiplied by 2024
                new.append(stone * 2024)

        orig = new

    return len(orig)

################################

@cache
def split(stone):
    name = str(stone)
    left = int(name[:len(name)//2])
    right = int(name[len(name)//2:])
    return left, right

@cache
def findNumDescendants(stone, blinks):
    """ 
    Find the number of descendants of a particular stone after a certain number of blinks
    """

    # if we've run out of blinks this stone is the last descendant
    if blinks == 0:
        return 1
    
    # if the stone's inscription is 0, it transforms into 1
    if stone == 0:
        # find the number of descendants of 1 after the remaining blinks
        return findNumDescendants(1, blinks - 1)
        
    # if the stone has an even number of digits, it splits in half
    if len(str(stone)) % 2 == 0:
        left, right = split(stone)
        # find the number of descendants of each half after the remaining blinks
        return findNumDescendants(left, blinks - 1) + findNumDescendants(right, blinks - 1)
        
    # otherwise, the stone's inscription is multiplied by 2024
    # find the number of descendants of the new stone after the remaining blinks
    return findNumDescendants(stone * 2024, blinks - 1)
    
def part2(data):
    """
    Find the total number of descendants of all stones after 75 blinks
    """
    # find the number of descendants of each stone after 75 blinks and add it to the total
    count = sum(findNumDescendants(stone, 75) for stone in data.line)

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