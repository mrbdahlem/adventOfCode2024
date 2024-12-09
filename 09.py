from collections import defaultdict
import helper
from datetime import datetime

day = int(__file__.split("\\")[-1].split("/")[-1].split(".")[0])
print ("Day", day)

tstart = datetime.now()

# load the data for this day (or a sample file)
data = helper.load_data(day)
# data = helper.load_data(f"{day:02}-samp")

desc = list(data.strip())

blocks = []
blocks2 = []

# Convert the data desc into blocks, alternating between file and freespace
nextFile = 0
isFile = True
for i in range(0, len(desc)):
    # The desc indicates the length of the file or free space
    length = int(desc[i])

    if isFile:
        file = nextFile # Each file is identified with a sequential number
        nextFile += 1
    else:
        file = -1

    # Add the file to the blocks list
    if (length > 0):
        # Part 2 - store the file and length for each block
        blocks2.append((file, length))

    # Part 1 - store the file number for each block
    for j in range(0, length):
        blocks.append(file)

    # Switch between file and free space
    isFile = not isFile

# The last file's id for part 2
lastFile = nextFile - 1

print("------------------------")
tparsed = datetime.now()

# Solve the first part

def calcChecksum(blocks):
    """
    Calculate the checksum of the blocks
    """
    checksum = 0
    # For each block, add the product of the file number and the block's position if the block is not free space
    for i in range(0, len(blocks)):
        if blocks[i] == -1:
            continue
        checksum += i * blocks[i]
    return checksum

# Sort the blocks by moving each block of each file to the first available position - breaking up the file
# so that it fits in any available space. Files will be moved starting from the end of the disk to the 
# beginning.
sorted = blocks.copy()
nextPos = 0 # the next position to move a file to
lastPos = len(sorted) - 1 # the position of a file to be moved

while nextPos < lastPos:
    # Find the next file block to move
    while sorted[lastPos] == -1 and lastPos > nextPos:
        lastPos -= 1

    # find the next available block to move to
    if sorted[nextPos] == -1:
        # If the next block is free space, move the file block to the next position
        sorted[nextPos] = sorted[lastPos]
        # Mark the original position as free space
        sorted[lastPos] = -1
        # move the file pointer to the next position
        lastPos -= 1
        
    # move the next position to the next block to look for free space
    nextPos += 1

# Calculate the checksum of the sorted blocks and print the result
checksum = calcChecksum(sorted)
print("Part 1: ", checksum)

tp1 = datetime.now()

# Solve the second part

def calcChecksum2(blocks):
    """ Calculate the checksum of the blocks which aren't free """
    checksum = 0
    pos = 0 # the current position in the disk

    for block in blocks:
        # If the block is free space, move the position pointer to the next block
        if block[0] == -1:
            pos += block[1]
            continue
        

        # Add the product of the file number and the position of each block in the file to the checksum
        for _ in range(0, block[1]):
            checksum += pos * block[0]
            pos += 1
    return checksum 

def find(id, blocks):
    """ Find the block with the given file id """
    for i, block in enumerate(blocks):
        if block[0] == id:
            return i, block

    return -1, None

def consolidate(loc, blocks):
    """ Consolidate the free blocks around the given location """
    # if the block before or after the location is free space, combine the blocks
    if loc < len(blocks) - 1 and blocks[loc + 1][0] == -1:
        blocks[loc] = (-1, blocks[loc][1] + blocks[loc + 1][1])
        blocks.pop(loc + 1)
    if loc > 0 and blocks[loc - 1][0] == -1:
        blocks[loc - 1] = (-1, blocks[loc - 1][1] + blocks[loc][1])
        blocks.pop(loc)

sorted = blocks2.copy()
nextPos = 0
lastPos = len(sorted) - 1
start = lastFile

# Move each file to the first available position in the disk, starting with the file at the end of the disk
for id in range(start, 0, -1):
    # find the next file to move
    oldPos, file = find(id, sorted)

    # find the next available position to move the file to
    for i, block in enumerate(sorted):
        if i >= oldPos:
            break
        
        # If the block is free space and is large enough to fit the file, move the file to the block
        if block[0] == -1 and block[1] >= file[1]:
            diff = block[1] - file[1]
            sorted[oldPos] = (-1, file[1])
            sorted[i] = file
            consolidate(oldPos, sorted) # consolidate the free space around the file's old position

            # If the free space is larger than the file
            if diff > 0:
                sorted.insert(i + 1, (-1, diff)) # insert the remaining free space after the file
                consolidate(i + 1, sorted) # consolidate the free space with any surrounding free space

            break

# Calculate the checksum of the sorted blocks and print the result
checksum = calcChecksum2(sorted)
print("Part 2: ", checksum)

tp2 = datetime.now()

print("------------------------")
print(f"Parse Time: {((tparsed - tstart).total_seconds() * 1000):.3f} ms")
print(f"Part 1 Time: {(tp1 - tparsed).total_seconds() * 1000:.3f} ms")
print(f"Part 2 Time: {(tp2 - tp1).total_seconds() * 1000:.3f} ms")