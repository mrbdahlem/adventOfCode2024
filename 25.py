from types import SimpleNamespace
import helper
import os

from copy import copy, deepcopy
from collections import defaultdict, deque
import re
from functools import cache
from PIL import Image, ImageDraw
import asyncio
import heapq

def countHeights(grid):
    heights = []
    for c in range(len(grid[0])):
        h = 0
        for r in range(len(grid)):
            if grid[r][c] == '#':
                h += 1
        heights.append(h - 1)
    return tuple(heights)
  
@helper.timeit
def parse(data):
    parsed = SimpleNamespace()

    schema = data.strip().split('\n\n')

    locks = []
    keys = []

    for schematic in schema:
        grid = [[c for c in line] for line in schematic.split('\n')]

        if grid[0][0] == '#':
            locks.append(countHeights(grid))
        else:
            keys.append(countHeights(grid))

    parsed.locks = locks
    parsed.keys = keys

    return parsed

################################

@helper.timeit
def part1(data):
    count = 0
    for lock in data.locks:
        for key in data.keys:
            match = 0
            for i in range(len(lock)):
                if lock[i] + key[i] > 5:
                    break
                match += 1
            if match == len(lock):
                count += 1  
    return count

################################

@helper.timeit
def part2(data):
    return 0

################################

def run(data, stage):
    """
    Run both parts of the day
    """
    parsed = parse(data)
    parsed.stage = stage
    print("-" * 24)
    
    # Solve the first part
    print("Part 1: {\033[0;41m\033[1;97m " + str(part1(parsed)) + " \033[0m}", part1Wrong[stage])


    # Solve the second part
    print("Part 2: {\033[0;42m\033[1;97m " + str(part2(parsed)) + " \033[0m}", part2Wrong[stage])

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

part1Wrong = {
    "samp": [],
    "full": []
}

part2Wrong = {
    "samp": [],
    "full": [(0, 'low'), (0, 'high')]
}


asyncio.run(main())