from types import SimpleNamespace
import helper
import os

from copy import copy, deepcopy
from collections import defaultdict
import re
from functools import cache
from PIL import Image, ImageDraw
import asyncio
import heapq

@helper.timeit
def parse(data):
    parsed = SimpleNamespace()
    parts = data.split("\n\n")

    parsed.towels = parts[0].strip().split(', ')
    parsed.designs = [d for d in parts[1].split('\n')]


    return parsed

################################
def matchPattern(design, towelPattern):

    if (re.match(towelPattern, design)):
        return 1
    
    return 0

@helper.timeit
def part1(data):

    # Create a regex pattern for all of the towels' stripe patterns
    towelPattern = '^(' + '|'.join(data.towels) + ')+$'
    data.towelPattern = re.compile(towelPattern)
    data.possible = []

    count = 0
    for design in data.designs:
        if re.match(data.towelPattern, design):
            count += 1
            data.possible.append(design)

    return count

################################

def findMatches(design, towels):
    """
    Find the number of ways the design can be made from the patterns on the towels
    """

    @cache
    def countMatches(design, start=0):
        """
        Recursively find the number of ways the design can be made from the towels
        """
        if start == len(design):
            return 1
        if start > len(design):
            return 0
        
        subDesign = design[start:]
        count = 0
        for towel in towels:
            if subDesign.startswith(towel):
                count += countMatches(design, start + len(towel))
        return count

    return countMatches(design)

@helper.timeit
def part2(data):

    # part 1 showed us which designs are possible, now we need to find how many ways they can be made
    count = 0
    for design in data.possible:
        count += findMatches(design, data.towels)

    return count

################################

def run(data, stage):
    """
    Run both parts of the day
    """
    parsed = parse(data)
    parsed.stage = stage
    print("-" * 24)
    
    # Solve the first part
    print("Part 1: {\033[0;41m\033[1;97m " + str(part1(parsed)) + " \033[0m}")

    # Solve the second part
    print("Part 2: {\033[0;42m\033[1;97m " + str(part2(parsed)) + " \033[0m}")

################################

async def main():
    sep = "~" * 56
    print(sep)

    # Get the day number from this file's name
    day = int(__file__.split(os.sep)[-1].split(".")[0])
    print (f"{f' Day {day} ':*^{len(sep)}}")
    print(sep)

    # load a sample data file for this day, if it exists
    if helper.exists(f"{day:02}-samp"):
        print(f"{' Sample Data ':-^{len(sep)}}")
        data = helper.load_data(f"{day:02}-samp")
        if data:
            run(data, 'samp')

    # load the actual data for this day
    print(f"{' Actual Data ':-^{len(sep)}}")

    data = helper.load_data(day)
    run(data, 'full')
    print(sep)

asyncio.run(main())