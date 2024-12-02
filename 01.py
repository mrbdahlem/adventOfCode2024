import helper

day = int(__file__.split("\\")[-1].split(".")[0])
print ("Day", day)

data = helper.load_data(day)

lines = data.splitlines()

left = []
right = []

for line in lines:
    parts = line.split('   ')
    left.append(int(parts[0]))
    right.append(int(parts[1]))

left.sort()
right.sort()

total = 0
for index in range(len(left)):
    diff = abs(left[index] - right[index])
    total += diff

print("Part 1:", total)

similarity = 0
for num in left:
    count = 0
    for poss in right:
        if num == poss:
            count += 1
    similarity += (num * count)

print ("Part 2:", similarity)

# 499500 - low


