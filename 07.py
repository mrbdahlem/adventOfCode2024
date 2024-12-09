import helper
from datetime import datetime

day = int(__file__.split("\\")[-1].split(".")[0])
print ("Day", day)

tstart = datetime.now()

# load the data for this day (or a sample file)
data = helper.load_data(day)
# data = helper.load_data(f"{day:02}-samp")

lines = data.split("\n")

# break each line down into an answer, and the numbers that form the equation
ans = [int(line.split(':')[0]) for line in lines if line != '']
eq = [line.split(':')[1].split(' ')[1:] for line in lines if line != '']
eq = [[int(x) for x in line] for line in eq]

print("------------------------")
tparsed = datetime.now()

# Solve the first part
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
        
# Solve the first part by counting the equations that can be calibrated to the answer using
# addition and multiplication
total = 0
for i in range(len(ans)):
    if (calibrate(ans[i], eq[i][1:], ['+', '*'], lambda: eq[i][0]) != False):
        total += ans[i]


print("Part 1: ", total)

tp1 = datetime.now()

# Solve the second part by counting the equations that can be calibrated to the answer using addition,
# multiplication, and concatenation
total2 = 0
for i in range(len(ans)):
    if (calibrate(ans[i], eq[i][1:], ['+', '*', '||'], lambda: eq[i][0]) != False):
        total2 += ans[i]

print("Part 2: ", total2)

tp2 = datetime.now()

print("------------------------")
print(f"Parse Time: {((tparsed - tstart).total_seconds() * 1000):.3f} ms")
print(f"Part 1 Time: {(tp1 - tparsed).total_seconds() * 1000:.3f} ms")
print(f"Part 2 Time: {(tp2 - tp1).total_seconds() * 1000:.3f} ms")