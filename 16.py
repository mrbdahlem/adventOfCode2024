from types import SimpleNamespace
import helper
from datetime import datetime

from copy import copy, deepcopy
from collections import defaultdict, deque
import re
from functools import cache
from PIL import Image, ImageDraw
import asyncio

def parse(data):
    parsed = SimpleNamespace()
    parsed.maze = [[c for c in line] for line in data.strip().split("\n")]
    
    for r in range(len(parsed.maze)):
        for c in range(len(parsed.maze[r])):
            if parsed.maze[r][c] == 'S':
                parsed.start = (r, c)
            if parsed.maze[r][c] == 'E':
                parsed.end = (r, c)

    return parsed

################################
opposite = {'e': 'w', 's': 'n', 'w': 'e', 'n': 's'}
dirs = {'e': (0, 1), 's': (1, 0), 'w': (0, -1), 'n': (-1, 0)}
turns = {'e': {'n': 1, 's': 1, 'w': 2, 'e': 0},
         's': {'e': 1, 'n': 2, 'w': 1, 's': 0},
         'w': {'e': 2, 'n': 1, 's': 1, 'w': 0},
         'n': {'e': 1, 's': 2, 'w': 1, 'n': 0}}

def drawMap(maze, nodes=[]):
    """
    Draw the map with the robot, boxes, and walls
    """
              
    # Create a new image with a white background
    img = Image.new('RGB', (len(maze[0]) * 10, len(maze)* 10), color='white')

    draw = ImageDraw.Draw(img)

    def rect(c, r, color):
        draw.rectangle((c * 10, r * 10, c * 10 + 10, r * 10 + 10), fill=color)
         
    for node in nodes:
        rect(node[1], node[0], (0, 255, 255))

    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == '#':
                rect(c, r, (0, 0, 0))
            elif maze[r][c] == 'S':
                rect(c, r, (0, 255, 0))
            elif maze[r][c] == 'E':
                rect(c, r, (255 , 0, 0))
    return img

def neighbors(node, dir, maze):
    """
    Find the neighbors of a node, the direction to get there, and the number of turns 
    required to get there
    """
    n = []
    r, c = node
    for d, (dr, dc) in dirs.items():
        nr, nc = r + dr, c + dc
        if maze[nr][nc] != '#':
            n.append(((nr, nc), d, turns[dir][d]))
    return n

def bestPath(start, end, maze, limit=99999999999):
    """
    Find the best path from the start to the end in the maze, with a cost <= the limit
    """
    cameFrom = dict()
    pos = start

    next=[pos] # priority queue of the nodes to explore, sorted by cost l>h
    while (pos[0] != end and next):
        # get the next node and the direction to get there
        pos = next.pop(0)
        dir = pos[3]

        # if we have already found a better path to this node, skip it
        if pos[0] in cameFrom:
            if pos[1] >= cameFrom[pos[0]][1]:
                continue

        # add the node to the list of nodes we have visited
        cameFrom[pos[0]]=(pos[2], pos[1], dir)
            
        # find the neighbors of the node
        for n,d,t in neighbors(pos[0], dir, maze):
            # if the cost of the path to the neighbor is less than the limit
            if (pos[1] + 1 + (t * 1000) <= limit):
                # add the neighbor to the list of nodes to explore
                next.append((n, pos[1] + 1 + (t * 1000), pos[0], d))

        # sort the list of nodes to explore by cost
        next = sorted(next, key=lambda x: x[1])

    # return the list of nodes we have visited and the cost to get to each from the start
    return cameFrom
    
def part1(data):
    # find the cost of the best path from start to the end
    start = (data.start, 0, None, 'e')
    cameFrom = bestPath(start, data.end, data.maze)
    data.pruned = cameFrom
    data.best = cameFrom[data.end][1]
    return data.best

################################
def findPaths(start, end, nodes, best, maze):
    """
    find all of the nodes that are on the paths from the start to the goal
    """
    pathNodes = set()
    pathNodes.add(start)
    pathNodes.add(end)

    l = len(nodes)
    # for each node in the list
    for i,n in enumerate(nodes):
        if n == start:
            continue
        if n == end:
            continue

        # if the node is further than the best path, skip it
        c = nodes[n][1]
        if c >= best:
            continue
        
        # find the best path from the node to the goal
        p = bestPath((n, c, nodes[n][0], nodes[n][2]), end, maze, best)

        # cost to the node and from the node to the end is on the best path
        if end in p and p[end][1] <= best:
            # add the node to the list of nodes on the path
            pathNodes.add(n)

        if (i % 100 == 0):
            print(f"{i}/{l}")

    return pathNodes

def part2(data):
    # find all of nodes on the paths from the start to the goal
    nodes = findPaths(data.start, data.end, data.pruned, data.best, data.maze)
    drawMap(data.maze, nodes).show()
    return len(nodes)
    

################################

def run(data, stage):
    """
    Run both parts of the day
    """
    tstart = datetime.now()
    parsed = parse(data)
    print("------------------------")
    tparsed = datetime.now()
    
    parsed.stage = stage
    
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

async def main():
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
        run(samp, 'samp')

    print("-------------------------------------------")
    run(data, 'full')

asyncio.run(main())