import helper
import re

day = int(__file__.split("\\")[-1].split(".")[0])
print ("Day", day)

data = helper.load_data(day)

# Find all the valid instructions
matches = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\)", data)

# Total up the multiplication instructions
total = 0
for cmd in matches:
    if cmd.startswith("mul"):
        a, b = map(int, cmd[4:-1].split(","))
        total += (a*b)

print("Part 1: ", total)

# Total up the multiplication instructions with the same logic as part 1,
# but skip the instructions between the don't and do commands
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