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

@helper.timeit
def parse(data):
    parsed = SimpleNamespace()
    parsed.data = data

    # break the map down into a 2D array
    parsed.map = [[c for c in line] for line in data.strip().splitlines()]

    # find the start and end points for the race
    for r in range(len(parsed.map)):
        for c in range(len(parsed.map[r])):
            if parsed.map[r][c] == 'S':
                parsed.start = (r, c)
            elif parsed.map[r][c] == 'E':
                parsed.end = (r, c)

    return parsed

################################

class Node:
    """
    A node in the bfsearch
    """
    def __init__(self, pos, prev, prevsteps):
        self.pos = pos
        self.prev = prev
        self.prevsteps = prevsteps

    def __lt__(self, other):
        return self.cost < other.cost

    def neighbors(self, map):
        """
        Find the neighbors of a node that are within the bounds of the map
        """
        n = []
        for d in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            x = self.pos[1] + d[1]
            y = self.pos[0] + d[0]
            if x >= 0 and x <= len(map[0]) and y >= 0 and y <= len(map) and map[y][x] != '#':
                n.append((y, x))
        return n

def bfs(start, end, map):
    """
    Find the shortest path from the start to the end avoiding the obstacles
    """
    start = Node(start, None, 0)
    visited = set()

    # add the start node to the queue of nodes to explore
    next = deque([start])
    
    node = start
    while (node.pos != end and next):
        # get the next node that is closest to the end
        node = next.popleft()

        # if we've already visited this node, skip it
        if node.pos in visited:
            continue

        # add the node to the list of nodes we have visited
        visited.add(node.pos)

        soFar = node.prevsteps + 1

        # find the neighbors of the node
        for n in node.neighbors(map):
            if (n in visited):
                continue
            # add the neighbor to the heap of nodes to explore
            next.append(Node(n, node, soFar))

    last = node

    # if we didn't reach the end, return None
    if last.pos != end:
        return None
    
    # otherwise, build the path from the end to the start
    path = []
    while last:
        path.append(last)
        last = last.prev

    return path

def dist(a, b):
    """
    Manhattan distance between two points
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def findShortcuts(path, maxShortcut, minSavings):
    """
    Find the shortcuts in the path that save at least minSavings steps
    """
    count = 0
    for i in range(len(path)):
        for j in range(i+1, len(path)):
            d = dist(path[i].pos, path[j].pos)
            if d <= maxShortcut and (path[i].prevsteps - path[j].prevsteps) - d >= minSavings:
                count += 1
    return count

@helper.timeit
def part1(data):

    if data.stage == 'samp':
        savings = 19
    else:
        savings = 100

    # Find the path from the start to the end
    path = bfs(data.start, data.end, data.map)
    data.path = path

    return findShortcuts(path, 2, savings)

################################

@helper.timeit
def part2(data):

    if data.stage == 'samp':
        savings = 50
    else:
        savings = 100

    path = data.path

    return findShortcuts(path, 20, savings)
    

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
    "full": [(945683, 'low'), (1071736, 'high')]
}

asyncio.run(main())