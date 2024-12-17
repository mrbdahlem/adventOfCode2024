from types import SimpleNamespace
import helper
from datetime import datetime

from copy import copy, deepcopy
from collections import defaultdict, deque
import re
from functools import cache
from PIL import Image, ImageDraw
import asyncio
import heapq

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
class DjNode:
    def __init__(self, pos, cost, prev, dir):
        self.pos = pos
        self.cost = cost
        self.prev = prev
        self.dir = dir

    def __lt__(self, other):
        return self.cost < other.cost

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

def djk(startNodes, end, maze):
    """
    find the distances from the start point to 'all' other points in the maze
    """
        
    visited = dict()

    # add the start node to the list of nodes to explore, with the ability to go in all directions
    next = copy(startNodes)

    node = next[0]
    while (node.pos != end and next):
        # get the next node and the direction to get there
        node = heapq.heappop(next)
        dir = node.dir

        # if we have already found a better path to this node, skip it
        if node.pos in visited and node.cost > visited[node.pos].cost:
            continue

        # add the node to the list of nodes we have visited
        visited[node.pos] = node
            
        # find the neighbors of the node
        for n,d,t in neighbors(node.pos, dir, maze):
            # add the neighbor to the heap of nodes to explore
            heapq.heappush(next, DjNode(n, node.cost + 1 + (t * 1000), node.pos, d))

    # return the list of nodes we have visited and the cost to get to each from the start
    return visited
    
def part1(data):
    # find the cost of the best path from start to the end
    start = [DjNode(data.start, 0, None, 'e')]
    
    data.forwards = djk(start, data.end, data.maze)
    data.best = data.forwards[data.end].cost

    return data.best

################################

def part2(data):
    """
    find all of nodes on the 'best' paths from the start to the goal
    """

    endNodes = [DjNode(data.end, 0, None, d) for d in dirs]

    forwards = data.forwards
    best = data.best

    # find the distance from the goal to 'all' of the nodes that
    backwards = djk(endNodes, data.start, data.maze)

    # find the nodes that are on the best paths
    pathNodes = set()

    # for each node found in the search from the end to the start and start to end
    for n in set(forwards.keys()).intersection(backwards.keys()):
        # if the cost of the path from the start to the node plus the cost of the path from
        # the node to the end is the same as the best path, it's on a best path
        if backwards[n].cost + forwards[n].cost == best:
            pathNodes.add(n)

        # if the node is on a turn, it's might also be on a best path
        elif (backwards[n].cost + forwards[n].cost + 
                (turns[backwards[n].dir][forwards[n].dir] * 1000) == best):
            pathNodes.add(n)
    
    drawMap(data.maze, pathNodes).save(f"output/day16{data.stage}-p2.png")

    return len(pathNodes)

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