import helper

day = int(__file__.split("\\")[-1].split("/")[-1].split(".")[0])
print ("Day", day)

data = helper.load_data(day)

lines = data.splitlines()

def checkSafe(line):
    ''' Check if the level changes in the given line are safe.
        Changes are safe if they are constantly decreasing or increasing, and
        the change is between 1 and 3 (inclusive).
    '''
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
    '''
    Check if the level changes in the given line are safe.
    At most one unsafe change is allowed.
    '''
    if checkSafe(line):
        return True
    
    levels = [int(x) for x in line.split(" ")]
    for index in range(0, len(levels)):
        newLevels = levels.copy()
        newLevels.pop(index)
        if checkSafe(" ".join([str(x) for x in newLevels])):
            return True
        
    return False

# Count the number of safe lines
safeCount = 0
for line in lines:    
    if checkSafe(line) == True:
        safeCount += 1

print("Part 1:", safeCount)

# Count the number of safe lines, allowing for one unsafe change
safeCount = 0
for line in lines:
    if checkSafe2(line) == True:
        safeCount += 1

print("Part 2:", safeCount)