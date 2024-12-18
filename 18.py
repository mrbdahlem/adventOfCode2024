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
    bytes = [line.strip().split(',') for line in data.strip().split('\n')]
    parsed.bytes = [(int(b[0]), int(b[1])) for b in bytes]

    maxX = 0
    maxY = 0
    for byte in parsed.bytes:
        if byte[0] > maxX:
            maxX = byte[0]
        if byte[1] > maxY:
            maxY = byte[1]

    parsed.maxX = maxX
    parsed.maxY = maxY
    return parsed

################################

def drawMap(path, obs, w, h, scale=10, visited=[]):
    """
    Draw the map with the robot, boxes, and walls
    """
    # Create a new image with a white background
    img = Image.new('RGB', ((w + 1) * scale, (h + 1) * scale), color='white')
    draw = ImageDraw.Draw(img)

    def point(c, r, color):
        draw.rectangle((c * scale, r * scale, c * scale + scale, r * scale + scale), fill=color)
    
    for p in obs:
        point(p[0], p[1], (255, 0, 0))

    for p in visited:
        point(p[0], p[1], (0, 0, 255))

    for p in path:
        point(p[0], p[1], (0, 255, 0))


    img.show()

    return img


class Node:
    """
    A node in the A* search
    """
    def __init__(self, pos, cost, prev, prevsteps):
        self.pos = pos
        self.cost = cost
        self.prev = prev
        self.prevsteps = prevsteps

    def __lt__(self, other):
        return self.cost < other.cost

def dist(a, b):
    """
    Find the Manhattan distance between two points
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(node, maxX, maxY):
    """
    Find the neighbors of a node that are within the bounds of the map
    """
    n = []
    for d in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        x = node[0] + d[0]
        y = node[1] + d[1]
        if x >= 0 and x <= maxX and y >= 0 and y <= maxY:
            n.append((x, y))
    return n
    
def astar(start, end, maxX, maxY, obstacles):
    """
    Find the shortest path from the start to the end avoiding the obstacles
    """
    start = Node(start, dist(start, end), None, 0)
    visited = set()

    # add the start node to the list of nodes to explore
    next = [start]
    heapq.heapify(next)

    node = start
    while (node.pos != end and next):
        # get the next node that is closest to the end
        node = heapq.heappop(next)
        
        # if we've already visited this node, skip it
        if node.pos in visited:
            continue

        # add the node to the list of nodes we have visited
        visited.add(node.pos)

        soFar = node.prevsteps + 1

        # find the neighbors of the node
        for n in neighbors(node.pos, maxX, maxY):
            # if the neighbor is an obstacle, skip it
            if n in obstacles:
                continue
            # add the neighbor to the heap of nodes to explore
            
            heapq.heappush(next, Node(n, soFar + dist(n, end), node, soFar))

    last = node

    # if we didn't reach the end, return None
    if last.pos != end:
        return None, visited
    
    # otherwise, build the path from the end to the start
    path = []
    while last:
        path.append(last.pos)
        last = last.prev

    return path, visited

@helper.timeit
def part1(data):
    """
    Find the shortest path from the start to the end avoiding a subset of the obstacles
    """
    start = (0, 0)
    maxX = data.maxX
    maxY = data.maxY
    end = (maxX, maxY)

    # only use the first 12 bytes for the sample data, the first 1024 bytes for the full data
    if (data.stage == 'samp'):
        bytes = set(data.bytes[:12])
    else:
        bytes = set(data.bytes[:1024])

    # find the shortest path from the start to the end
    best, visited = astar(start, end, maxX, maxY, bytes)

    # remember the path for part 2
    data.path = best

    # drawMap(best, bytes, maxX, maxY, visited=visited)

    # return the length of the path (ignoring the start node)
    return len(best) - 1


################################

@helper.timeit
def part2(data):
    """
    Find the first obstacle that causes the path to be blocked
    """
    # Same starting and ending points
    start = (0, 0)
    maxX = data.maxX
    maxY = data.maxY
    end = (maxX, maxY)

    # start with the path from part 1
    path = data.path
    
    # Start at byte 12 for the sample data, byte 1024 for the full data
    if (data.stage == 'samp'):
        sb = 12
    else:
        sb = 1024

    obstacles = set(data.bytes[:sb])

    # add one obstacle at a time and see if there is still a path to the end
    for i,byte in enumerate(data.bytes[sb:]):
        obstacles.add(byte)
        if byte in path: # if the path gets blocked
            # find the new shortest path from the start to the end
            newPath, _ = astar(start, end, maxX, maxY, obstacles)
            
            # drawMap(newPath, data.bytes[0:i+sb+1], maxX, maxY)
            if newPath == None: # if there is no path remaining
                return f"{byte[0]},{byte[1]}" # return the coordinates of the obstacle that blocked the path

            path = newPath

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
    # exit()
    # load the actual data for this day
    print(f"{' Actual Data ':-^{len(sep)}}")

    data = helper.load_data(day)
    run(data, 'full')
    print(sep)

asyncio.run(main())