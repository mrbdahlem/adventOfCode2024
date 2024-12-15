from types import SimpleNamespace
import helper
from datetime import datetime

from copy import copy, deepcopy
from collections import defaultdict
import re
from functools import cache
from PIL import Image, ImageDraw, ImageFont
import asyncio

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
async def saveImage(images, name, width, height):
    """
    Save a list of images as a contact sheet
    """
    imgwidth, imgheight = images[0].size

    img = Image.new('RGB', (width * (imgwidth + 1), height * (imgheight + 1)), color='white')

    for x in range(width):
        for y in range(height):
            img.paste(images[x + y * width], (x * (imgwidth + 1), y * (imgheight + 1)))
    img.save(name)

def robotMap(robots, w, h, name='', num=None):
    """
    Save a map of the robots
    """
    # Create a new image with a black background
    img = Image.new('RGB', (w, h), color='black')

    # mark the robots on the image
    pixels = img.load()
    for robot in robots:
        pixels[robot.pos[0], robot.pos[1]] = (0,255,0)
    
    # if a frame number is provided, add it to the image
    if num != None:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('DejaVuSansMono.ttf', 10)
        draw.text((0, 0), f"{num}", fill=(255, 255, 255), font=font)

    if name:
        img.save(name)

    return img


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

def findCluster(robot, robots, size):
    for d in range(1, size):
        if not (robot.pos[0] + d, robot.pos[1]) in robots or not (robot.pos[0], robot.pos[1] + d) in robots:
            return False
    return True


def part2(data):
    """
    Move the robots until they form a cluster, hopefully in the form of an easter egg, then determine the time it took
    """
    ans = set()

    # Reset the robots to their original positions
    for rob in data.robots:
        rob.reset()

    data.images = [robotMap(data.robots, data.w, data.h, num=0)]

    # Move the robots repeatedly, looking for a loop in x and y positions to determine an
    # upper bound on the number of iterations
    stateOne = []
    xloop = None
    yloop = None
    i = 1
    while(not (xloop and yloop) or i < xloop * yloop):
        pos = set()
        cluster = False
        # Move the robots repeatedly, looking for small clusters
        for r,robot in enumerate(data.robots):
            robot.move(data.w, data.h)
            pos.add(robot.pos)
            if i == 1:
                stateOne.append(robot.pos)
            else:
                if not xloop:
                    # compare the current state to the first state
                    if robot.pos[0] == stateOne[r][0]:
                        xloop = i-1
                        data.xloop=xloop
                        print(f"Found a loop in x at {xloop} iterations")
                
                # Check for a loop in the y positions of the robots
                if not yloop:
                    # compare the current state to all the first state
                    if robot.pos[1] == stateOne[r][1]:
                        yloop = i-1
                        data.yloop=yloop
                        print(f"Found a loop in y at {yloop} iterations")

            if r % 2 == 0:
                # Check for a cluster of robots of size 'size'
                cluster = cluster or findCluster(robot, pos, 7)

        # If the robot is close to a bunch of other robots, add it to the answer, and create a snapshot of the robots
        if cluster:
            # Record the number of iterations
            ans.add(i)
            print(f"!!!!{i}!!!!")
            robotMap(data.robots, data.w, data.h, name=f'data/day14{data.stage}-{i}.png')

        data.images.append(robotMap(data.robots, data.w, data.h, num=i))

        # Print a status message every 200 iterations
        if (i % 500 == 0):
            print(i)

        i += 1

    return ans

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

    asyncio.create_task(saveImage(parsed.images, f'data/day14{stage}.png', width=parsed.xloop, height=parsed.yloop))


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