import copy
import helper
from datetime import datetime
from collections import defaultdict

day = int(__file__.split("\\")[-1].split("/")[-1].split(".")[0])
print ("Day", day)

tstart = datetime.now()

# load the data for this day (or a sample file)
data = helper.load_data(day)
# data = helper.load_data(f"{day:02}-samp")
lines = data.splitlines()
mp = [list(x) for x in lines]

for r in range(len(mp)):
    for c in range(len(mp[r])):
        if mp[r][c] == "^":
            start = (r, c)

print("------------------------")
tparsed = datetime.now()

# Solve the first part
def nextPos(r, c, dir):
    """ Return the next position given the current position and direction of travel """
    nr = r
    nc = c
    if (dir == 'u'):
        nr = r - 1
    elif (dir == 'd'):
        nr = r + 1
    elif (dir == 'l'):
        nc = c - 1
    elif (dir == 'r'):
        nc = c + 1

    return nr, nc

def nextDir(dir):
    """ Return the next direction to turn given the current direction """
    if (dir == 'u'):
        return 'r'
    elif (dir == 'r'):
        return 'd'
    elif (dir == 'd'):
        return 'l'
    elif (dir == 'l'):
        return 'u'
    
path = defaultdict(list)
r, c = start
dir = "u"

# loop until we exit the map
while (r >= 0 and r < len(mp)) and (c >= 0 and c < len(mp[r])):
    path[(r, c)].append(dir)

    # check if we can move forward or if there is an obsticle and we need to turn
    nr, nc = nextPos(r, c, dir)
    ndir = dir
    while (nr >= 0 and nr < len(mp)) and (nc >= 0 and nc < len(mp[nr])) and mp[nr][nc] == "#":
        ndir = nextDir(ndir)
        nr, nc = nextPos(r, c, ndir)

    r, c, dir = nr, nc, ndir

print("Part 1: ", len(path))

tp1 = datetime.now()

# Solve the second part

def loop(obsR, obsC):
    """ Check if the path from the starting point loops back on itself if an obsticle has been added at (obsR, obsC) """
    visited = set()
    r, c = start
    dir = 'u'
    
    # loop until we exit the map
    while (r >= 0 and r < len(mp)) and (c >= 0 and c < len(mp[r])):
        # if we have visited this point before, moving in the current direction, we have a loop
        if (r, c, dir) in visited:
            return True
        
        # mark this point as visited
        visited.add((r, c, dir))

        # check if we can move forward or if there is an obsticle and we need to turn
        nr, nc = nextPos(r, c, dir)
        ndir = dir
        while ((nr >= 0 and nr < len(mp)) and (nc >= 0 and nc < len(mp[nr])) and 
               (mp[nr][nc] == "#" or (nr==obsR and nc==obsC))):
            ndir = nextDir(ndir)
            nr, nc = nextPos(r, c, ndir)

        r, c, dir = nr, nc, ndir

    # if we exit the map, we do not have a loop
    return False

obs = set()
r, c = start
dir = "u"
# check each point in the path to see, if we place an obsticle there, do we get a loop?
for point in path.keys():
    if point == start:
        continue

    if loop(point[0], point[1]):
        obs.add(point)

print("Part 2: ", len(obs), "- 1025 low, !1510, !1596")

tp2 = datetime.now()

print("------------------------")
print(f"Parse Time: {((tparsed - tstart).total_seconds() * 1000):.3f} ms")
print(f"Part 1 Time: {(tp1 - tparsed).total_seconds() * 1000:.3f} ms")
print(f"Part 2 Time: {(tp2 - tp1).total_seconds() * 1000:.3f} ms")