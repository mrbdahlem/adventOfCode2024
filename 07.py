from types import SimpleNamespace
import helper
from datetime import datetime

def parse(data):
    parsed = SimpleNamespace()
    
    lines = data.split("\n")

    # break each line down into an answer, and the numbers that form the equation
    parsed.ans = [int(line.split(':')[0]) for line in lines if line != '']
    eq = [line.split(':')[1].split(' ')[1:] for line in lines if line != '']
    parsed.eq = [[int(x) for x in line] for line in eq]
    return parsed

################################

def calibrate (ans, nums, ops, eq):
    """ 
    Recursively determine the correct order of operations so the equation equals the answer
    """
    # if there are no more numbers, check if the equation equals the answer
    if len(nums) == 0:
        if eq() == ans:
            return True
        return False
        
    # for each operation, try to find the next operation that will use with the next number to get the answer
    # after recursively checking the rest of the numbers and operations
    for op in ops:
        if op == '+': 
            if calibrate(ans, nums[1:], ops, lambda: eq() + nums[0]) == True:
                return True
            
        elif op == '*':
            if calibrate(ans, nums[1:], ops, lambda: eq() * nums[0]) == True:
                return True
            
        elif op == '||':
            if calibrate(ans, nums[1:], ops, lambda: int(str(eq()) + str(nums[0]))) == True:
                return True
            
    return False

def part1(data):
    total = 0
    for i in range(len(data.ans)):
        if (calibrate(data.ans[i], data.eq[i][1:], ['+', '*'], lambda: data.eq[i][0]) != False):
            total += data.ans[i]
    return total

################################

def part2(data):
    total = 0
    for i in range(len(data.ans)):
        if (calibrate(data.ans[i], data.eq[i][1:], ['+', '*', '||'], lambda: data.eq[i][0]) != False):
            total += data.ans[i]
    return total

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

if samp:
    print("--------------- Sample Data ---------------")
    run(samp)
print("-------------------------------------------")
run(data)