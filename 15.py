from types import SimpleNamespace
import helper
from datetime import datetime

from copy import copy, deepcopy
from collections import defaultdict
import re
from functools import cache
from PIL import Image
import asyncio

def parse(data):
    parsed = SimpleNamespace()
    
    parts = data.strip().split("\n\n")
    
    parsed.map = [[c for c in line] for line in parts[0].split("\n")]
    parsed.moves = "".join(parts[1].split("\n"))

    # Find the robot's starting location, and the locations of the boxes and wall segments
    parsed.boxes = set()
    parsed.walls = set()
    for r in range(len(parsed.map)):
        for c in range(len(parsed.map[r])):
            if parsed.map[r][c] == '@':
                parsed.start = (r, c)
            if parsed.map[r][c] == 'O':
                parsed.boxes.add((r, c))
            if parsed.map[r][c] == '#':
                parsed.walls.add((r, c))
    
    parsed.w = len(parsed.map[0])
    parsed.h = len(parsed.map)

    return parsed

################################
async def saveGif(images, name):
    """
    Save a list of images as a GIF
    """
    images[0].save(name, save_all=True, append_images=images[1:], duration=100, loop=0)

def drawMap(robot, boxes, walls, w, h):
    """
    Draw the map with the robot, boxes, and walls
    """
    # Create a new image with a white background
    img = Image.new('RGB', (w, h), color='white')

    # mark the robots on the image
    pixels = img.load()

    for w in walls:
        pixels[w[1], w[0]] = (0, 0, 255)

    for b in boxes:
        pixels[b[1], b[0]] = (0, 255, 0)
        if (len(b) == 3):
            pixels[b[2], b[0]] = (0, 255, 0)
                                  
    pixels[robot[1], robot[0]] = (255, 0, 0)

    return img

dirs = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}

def checkBoxes(source, dr, dc, boxes, walls):
    """
    Check if the robot can push boxes in the direction specified
    """
    # if the robot (or box) is trying to move into a box
    if source in boxes:
        # print("checking box at", source)
        # find the new location of the box
        new_box = (source[0] + dr, source[1] + dc)

        # if the new location is a wall, the box can't move
        if new_box in walls:
            # print("Can't move box into wall")
            return False # box can't move, so push failed
        
        # If the box can safely move (it won't push into a wall or a chain that is blocked)
        if checkBoxes(new_box, dr, dc, boxes, walls):    
            # move the box to the new location
            boxes.remove(source)
            boxes.add(new_box)
            # print("Moved box", source, "to", new_box)
            return True
        
        # print("Can't move box", source, "to", new_box)
        return False # box can't move, so push failed
    
    # print("No box to move")
    return True # no box to push, so we can move

def calcScore(boxes):
    """
    Calculate the score of the boxes (100 * row + column)
    """
    total = 0

    for b in boxes:
        total += b[0]*100 + b[1]
    return total


def part1(data):
    """
    Solve part 1 by moving the robot and boxes around the map 
    """
    robot = data.start
    boxes = copy(data.boxes)
    walls = copy(data.walls)

    # Create a new image of the initial map
    data.animation.append(drawMap(robot, boxes, walls, data.w, data.h))

    # simulate each move in the robot's program
    for i,move in enumerate(data.moves):
        # print("Move", i+1, move)
        dr, dc = dirs[move]
        new_robot = (robot[0] + dr, robot[1] + dc)
        
        if new_robot in walls:
            # print("Can't move into wall")
            continue
        
        # if the robot can successfully push the box, move the robot
        if checkBoxes(new_robot, dr, dc, boxes, walls):
           robot = new_robot

        data.animation.append(drawMap(robot, boxes, walls, data.w, data.h))

    # draw the final map
    data.animation.append(drawMap(robot, boxes, walls, data.w, data.h))

    return calcScore(boxes)

################################

def embiggen(boxes, walls):
    """
    Stretch the width of the map including the boxes and walls
    """

    new_boxes = set()
    new_walls = set()

    for b in boxes:
        new_boxes.add((b[0], b[1] * 2, b[1] * 2 + 1))
    for w in walls:
        new_walls.add((w[0], w[1] * 2))
        new_walls.add((w[0], (w[1] * 2) + 1))

    return new_boxes, new_walls

def boxAt(boxes, r, c):
    """
    Find the box at the specified row and column
    """
    for b in boxes:
        if b[0] == r and b[1] == c:
            return b
        if b[0] == r and b[2] == c:
            return b
    return None

def checkBoxes2(source, dr, dc, boxes, walls):
    """
    Check if the robot can push double wide boxes in the direction specified
    """
    if (source[0], source[1]) in walls or (source[0], source[2]) in walls:
        # print("Can't move box into wall")
        return False # box can't move, so push failed
    
    b = None
    c = None

    if dr != 0:
        b = boxAt(boxes, source[0], source[1])
        c = boxAt(boxes, source[0], source[2])
    elif dc == -1:
        b = boxAt(boxes, source[0], source[1])
    elif dc == 1:
        b = boxAt(boxes, source[0], source[2])

    if not b and not c:
        # print("No box to move")
        return True
    
    if b:
        # print("checking box at", b, dr)
        newB = (b[0] + dr, b[1] + dc, b[2] + dc)
        boxes.remove(b)
        if checkBoxes2(newB, dr, dc, boxes, walls):
            boxes.add(newB)
        else:
            return False
    
    if dr != 0 and c and c != b:
        # print("checking box at", c)
        newC = (c[0] + dr, c[1] + dc, c[2] + dc)
            
        boxes.remove(c)
        if checkBoxes2(newC, dr, dc, boxes, walls):
            boxes.add(newC)
        else:
            return False
        
    return True


def part2(data):
    """
    Solve part 2 by moving the robot and double wide boxes around the map
    """
    robot = (data.start[0], data.start[1] * 2)
    boxes, walls = embiggen(data.boxes, data.walls)

    # draw the initial (double wide) map
    data.animation.append(drawMap(robot, boxes, walls, data.w * 2, data.h))

    # simulate each move in the robot's program
    for i,move in enumerate(data.moves):
        dr, dc = dirs[move]
        # print("Move", i+1, move, dr, dc)

        # find the new location of the robot
        newRobot = (robot[0] + dr, robot[1] + dc)
        # print ("New Robot", newRobot, walls)

        if newRobot in walls:
            # print("Can't move into wall")
            continue
        
        # check if the robot can push the double wide boxes without pushing them into walls
        newBoxes = copy(boxes)
        if checkBoxes2((newRobot[0], newRobot[1], newRobot[1]), dr, dc, newBoxes, walls):
           robot = newRobot
           boxes = newBoxes
        data.animation.append(drawMap(robot, boxes, walls, data.w * 2, data.h))

    # draw the final map
    data.animation.append(drawMap(robot, boxes, walls, data.w * 2, data.h))

    return calcScore(boxes)

################################

def run(data, stage):
    """
    Run both parts of the day
    """
    tstart = datetime.now()
    parsed = parse(data)
    parsed.stage = stage
    print("------------------------")
    tparsed = datetime.now()
    
    parsed.animation = []

    # Solve the first part
    print("Part 1: ", part1(parsed))
    tp1 = datetime.now()

    print("Saving GIF", end='')
    asyncio.create_task(saveGif(parsed.animation, f'data/day15{stage}-p1.gif'))
    print(" - Done")
    parsed.animation = []

    # Solve the second part
    print("Part 2: ", part2(parsed))
    tp2 = datetime.now()

    print("Saving GIF", end='')
    asyncio.create_task(saveGif(parsed.animation, f'data/day15{stage}-p2.gif'))
    print(" - Done")

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