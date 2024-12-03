import helper
import re

day = int(__file__.split("\\")[-1].split(".")[0])
print ("Day", day)

data = helper.load_data(day)

matches = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\)", data)

total = 0
for cmd in matches:
    if cmd.startswith("mul"):
        a, b = map(int, cmd[4:-1].split(","))
        total += (a*b)

print("Part 1: ", total)

total = 0
enabled = True
for cmd in matches:
    if (cmd.startswith("don")):
        enabled = False
    elif (cmd.startswith("do")):
        enabled = True
    elif enabled and cmd.startswith("mul"):
        a, b = map(int, cmd[4:-1].split(","))
        total += (a*b)

print("Part 2: ", total)