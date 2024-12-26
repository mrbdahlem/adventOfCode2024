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

dirs = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}

class Key:
    def __init__(self, name, row, col):
        self.name = name
        self.row = row
        self.col = col

def graph(data):    
    grid = [[c for c in line] for line in data.split('\n')]

    keys = dict()

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            key = Key(grid[r][c], r, c)
            keys[key.name] = key

    return keys

@helper.timeit
def parse(data):
    parsed = SimpleNamespace()
    parsed.codes = data.strip().split('\n')

    numpad = '789\n456\n123\n 0A'
    dirpad = ' ^A\n<v>'

    parsed.numpad = graph(numpad)
    parsed.dirpad = graph(dirpad)

    return parsed

################################
class InvalidSpace(Exception):
    pass

def changeRow(row, d, col, pad):
    if row < d:
        dr = ('v',1)
    elif row > d:
        dr = ('^',-1)
    else:
        dr = ('',0)

    path = []
    while row != d:
        path.append(dr[0])
        row += dr[1]

        bad = pad[' ']
        
        if bad.row == row and bad.col == col:
            raise InvalidSpace('Invalid path')

    return path

def changeCol(col, d, row, pad):
    if col < d:
        dc = ('>',1)
    elif col > d:
        dc = ('<',-1)
    else:
        dc = ('',0)

    bad = pad[' ']

    path = []
    while col != d:
        path.append(dc[0])
        col += dc[1]

        if bad.row == row and bad.col == col:
            raise InvalidSpace('Invalid path')

    return path

def findPaths(currentKey, destKey, pad):
    if currentKey == destKey:
        return ''
        
    current = pad[currentKey]
    dest = pad[destKey]

    paths = set()

    try:
        paths.add(tuple(changeRow(current.row, dest.row, current.col, pad) + changeCol(current.col, dest.col, dest.row, pad)))
    except InvalidSpace as e:
        pass
    
    try:
        paths.add(tuple(changeCol(current.col, dest.col, current.row, pad) + changeRow(current.row, dest.row, dest.col, pad)))
    except InvalidSpace as e:
        pass

    return paths


def findSequence(code, dirpad, numpad):
    last = 'A'
    path = []
    for d in code:
        path += [findPaths(last, d, dirpad)]
        last = d

    return path

@helper.timeit
def part1(data):

    for code in data.codes:
        print(code)
        num = int(code[:-1])

        seq = findSequence(code, data.numpad, 1)
    
        print (seq)
    return 0

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

    exit()
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
    "full": [(945683, 'low'), (1071736, 'high')]
}


asyncio.run(main())