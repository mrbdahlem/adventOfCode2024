from types import SimpleNamespace
import helper
from datetime import datetime

from copy import copy, deepcopy
from collections import defaultdict
import re
from functools import cache
from PIL import Image
import math

class Robot:
    """
    A robot has a position and moves at a fixed velocity, wrapping around the edges of the grid
    """
    def __init__(self, data):
        # split the data into position and velocity
        parts = data.split(' ')

        # extract the position and velocity
        px, py = map(int, re.findall(r'-?\d+', parts[0]))
        vx, vy = map(int, re.findall(r'-?\d+', parts[1]))
        self.pos = (px, py)             
        self.vel = (vx, vy)

        # store the original position for part 2
        self.originalPos = self.pos

    def move(self, mx, my):
        """
        Move the robot by its velocity, wrapping around the edges of the grid
        """
        x, y = self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]
        self.pos = (x % mx, y % my)

    def reset(self):
        """
        Reset the robot to its original position
        """
        self.pos = self.originalPos


def parse(data):
    parsed = SimpleNamespace()
    lines = data.strip().split('\n')
    parsed.robots = [Robot(line) for line in lines]

    # Determine the width and height of the grid
    parsed.w = max([robot.pos[0] for robot in parsed.robots]) + 1
    parsed.h = max([robot.pos[1] for robot in parsed.robots]) + 1
    return parsed

################################
def robotMap(robots, w, h, name=''):
    """
    Save a map of the robots
    """
    # Create a new image with a white background
    img = Image.new('RGB', (w, h), color='white')

    # mark the robots on the image
    pixels = img.load()
    for robot in robots:
        pixels[robot.pos[0], robot.pos[1]] = (0,255,0)
    
    # Save the image
    img.save(f'data/img{name}.png')


def safety(robots, w, h):
    """
    Determine the safety number, the number of robots in each quadrant multiplied together
    """
    q=[0, 0, 0, 0]

    # Determine the number of robots in each quadrant, ignoring any on the center lines
    for robot in robots:
        if (robot.pos[0] < w // 2):
            if (robot.pos[1] < h // 2):
                q[0] += 1 
            elif (robot.pos[1] > h // 2):
                q[2] += 1
        elif (robot.pos[0] > w // 2):
            if (robot.pos[1] < h // 2):
                q[1] += 1
            elif (robot.pos[1] > h // 2):
                q[3] += 1
            
    return q[0] * q[1] * q[2] * q[3]

def part1(data):
    """
    Move the robots 100 times then determine the safety number
    """
    for _ in range(100):
        for robot in data.robots:
            robot.move(data.w, data.h)

    return safety(data.robots, data.w, data.h)

################################

def part2(data):
    """
    Move the robots until they form a cluster, hopefully in the form of an easter egg, then determine the time it took
    """
    ans = set()

    # Reset the robots to their original positions
    for r in data.robots:
        r.reset()

    
    # Move the robots repeatedly, looking for a loop in x and y positions to determine an
    # upper bound on the number of iterations
    locs = []
    xloop = None
    yloop = None
    i = 0
    while(not (xloop and yloop)):
        loc = []

        # Move the robots
        for robot in data.robots:
            robot.move(data.w, data.h)
            loc.append(robot.pos)

        # Check for a loop in the x positions of the robots    
        if not xloop:
            # compare the current location to all previous locations
            for k,l in enumerate(locs):
                loop = True
                for j,r in enumerate(data.robots):
                    if r.pos[0] != l[j][0]:
                        loop = False
                        break
                if loop:
                    print(f"Found a loop in x at {i} from {k} of {i-k} iterations")
                    xloop = (k, i-k)
                    break
        # Check for a loop in the y positions of the robots
        if not yloop:
            # compare the current location to all previous locations
            for k,l in enumerate(locs):
                loop = True
                for j,r in enumerate(data.robots):
                    if r.pos[1] != l[j][1]:
                        loop = False
                        break
                if loop:
                    print(f"Found a loop in y at {i} from {k} of {i-k} iterations")
                    yloop = (k, i-k)
                    break

        locs.append(loc)
        i+=1
        
    # Reset the robots to their original positions
    for r in data.robots:
        r.reset()

    size = 8
    # Move the robots repeatedly, looking for small clusters
    for i in range (1, xloop[1] * yloop[1]):
        pos = set()
        # Move the robots, record their new positions
        for robot in data.robots:
            robot.move(data.w, data.h)
            pos.add((robot.pos[0], robot.pos[1]))
        
        # Check for a cluster of robots of size 'size'
        for robot in data.robots:
            count = 0
            for d in range(1, size):
                if (robot.pos[0] + d, robot.pos[1]) and (robot.pos[0], robot.pos[1] + d) in pos:
                    count += 1
                else:
                    break

            # If the robot is close to a bunch of other robots, add it to the answer, and create a snapshot of the robots
            if count == size - 1:
                # Record the number of iterations
                ans.add(i)
                print(f"!!!!{i}!!!!")
                robotMap(data.robots, data.w, data.h, i)                
                break

        # Print a status message every 200 iterations
        if (i % 200 == 0):
            print(i)

    return ans

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

# if samp:
#     print("--------------- Sample Data ---------------")
#     run(samp)
print("-------------------------------------------")
run(data)