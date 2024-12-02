import helper
import re

data = helper.load_data(2)

lines = data.splitlines()

def checkSafe(line):
    levels = [int(x) for x in line.split(" ")]
    
    dir = None
    for index in range(1, len(levels)):
        dist = levels[index] - levels[index - 1]
        stepDir = -1 if dist < 0 else 1

        if dir == None:
            dir = stepDir
        elif dir != stepDir:
            return False

        dist = abs(dist)
        if dist < 1 or dist > 3:
            return False
        
    return True

def checkSafe2(line):
    if checkSafe(line):
        return True
    
    levels = [int(x) for x in line.split(" ")]
    for index in range(0, len(levels)):
        newLevels = levels.copy()
        newLevels.pop(index)
        if checkSafe(" ".join([str(x) for x in newLevels])):
            return True
        
    return False
    
safeCount = 0
for line in lines:    
    if checkSafe(line) == True:
        safeCount += 1

print("Part 1:", safeCount)

safeCount = 0
for line in lines:
    if checkSafe2(line) == True:
        safeCount += 1

print("Part 2:", safeCount)