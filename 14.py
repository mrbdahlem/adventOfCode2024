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
    def __init__(self, data):
        parts = data.split(' ')
        px, py = map(int, re.findall(r'-?\d+', parts[0]))
        vx, vy = map(int, re.findall(r'-?\d+', parts[1]))
        pos = (px, py)             
        vel = (vx, vy)
        self.originalPos = pos
        self.pos = pos
        self.vel = vel

        # print (self.pos, self.vel)
    
    def move(self, mx, my):
        x, y = self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]
        x %= mx
        y %= my
        self.pos = (x, y)

    def reset(self):
        self.pos = self.originalPos


def parse(data):
    parsed = SimpleNamespace()
    lines = data.strip().split('\n')
    parsed.robots = [Robot(line) for line in lines[1:]]
    parsed.w, parsed.h = map(int, lines[0].split(","))
    return parsed

################################
def robotMap(robots, w, h):
    for r in range(h):
        for c in range(w):
            count = 0
            for robot in robots:
                if robot.pos == (c, r):
                    count += 1
            if r != h // 2:
                if c != w // 2 and count != 0:
                    print (count, end='')
                else:
                    print (' ', end='')

        if r == h // 2:
            print ()
        print()


def safety(robots, w, h):
    q=[0, 0, 0, 0]

    # print(robotMap(robots, w, h))
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
            
    # print(q, sum(q))
    return q[0] * q[1] * q[2] * q[3]

def part1(data):
    for _ in range(100):
        for robot in data.robots:
            robot.move(data.w, data.h)
    
    return safety(data.robots, data.w, data.h)

################################

def part2(data):
    ans = set()

    for r in data.robots:
        r.reset()

    for i in range (1, 10000):

        for robot in data.robots:
            robot.move(data.w, data.h)

        for n, robot in enumerate(data.robots):
            count = 0
            for robot2 in data.robots[n+1:]:
                if math.dist(robot.pos, robot2.pos) < 5:
                    count+=1

            if count > 30:
                ans.add(i)
                # Create a new image with a white background
                img = Image.new('RGB', (data.w, data.h), color='white')

                # Get the pixel access object
                pixels = img.load()

                for robot in data.robots:
                    pixels[robot.pos[0], robot.pos[1]] = (0,255,0)
                
                # Save the image
                img.save(f'data/img{i}.png')

        if (i % 200 == 0):
            print(i)
        # robotMap(data.robots, data.w, data.h)
        # print (i)
        # input()

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