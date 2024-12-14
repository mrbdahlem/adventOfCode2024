from types import SimpleNamespace
import helper
from datetime import datetime

from copy import copy, deepcopy
from collections import defaultdict
import re
from functools import cache

def machine(data):
    m = SimpleNamespace()
    lines = data.split("\n")

    num = r"(\d+)"

    m.ax, m.ay = [int(x) for x in re.findall(num, lines[0])]
    m.bx, m.by = [int(x) for x in re.findall(num, lines[1])]
    m.px, m.py = [int(x) for x in re.findall(num, lines[2])]

    return m

def parse(data):
    parsed = SimpleNamespace()
    parts = data.strip().split("\n\n")

    parsed.machines = [machine(part) for part in parts]

    return parsed

################################
def solve(m):
    d = (m.ax*m.by - m.bx*m.ay)
    a = (m.px*m.by - m.bx*m.py) / d

    if a < 0 or not a.is_integer():
        return None

    b = (m.ax*m.py - m.ay*m.px) / d

    if b < 0 or not b.is_integer():
        return None
    
    return int(a*3 + b)

def part1(data):
    total = 0
    for m in data.machines:
        if (s := solve(m)) is not None:
            total += s

    return total

################################

def part2(data):
    total = 0
    for m in data.machines:
        m.px += 10000000000000
        m.py += 10000000000000
        if (s := solve(m)) is not None:
            total += s

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