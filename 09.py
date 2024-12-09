from types import SimpleNamespace
import helper
from datetime import datetime

def parse(data):
    parsed = SimpleNamespace()
    parsed.blocks = [] 
    parsed.blocks2 = [] 

    desc = list(data.strip())

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
            parsed.blocks2.append(Block(id=file, length=length))

        # Part 1 - store the file number for each block
        for _ in range(0, length):
            parsed.blocks.append(file)

        # Switch between file and free space
        isFile = not isFile

    # The last file's id for part 2
    parsed.lastFile = nextFile - 1

    return parsed

################################

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

def part1(data):
    # Sort the blocks by moving each block of each file to the first available position - breaking up the file
    # so that it fits in any available space. Files will be moved starting from the end of the disk to the 
    # beginning.
    sorted = data.blocks
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
    return calcChecksum(sorted)

################################

class Block:
    def __init__(self, id, length):
        self.id = id
        self.length = length

def calcChecksum2(blocks):
    """ Calculate the checksum of the blocks which aren't free """
    checksum = 0
    pos = 0 # the current position in the disk

    for block in blocks:
        # If the block is not free space, 
        if block.id != -1:
            # add the product of the file number and the position of EACH block in the file to the checksum
            checksum += int((block.length / 2) * (2 * pos + block.length - 1)) * block.id
        # move the position to the beginning of the next block
        pos += block.length

    return checksum 

def find(id, blocks):
    """ Find the block with the given file id """
    for i, block in enumerate(blocks):
        if block.id == id:
            return i, block

    return -1, None

def consolidate(loc, blocks):
    """ Consolidate the free blocks around the given location """
    # if the block before or after the location is free space, combine the blocks
    if loc < len(blocks) - 1 and blocks[loc + 1].id == -1:
        blocks[loc] = Block(id = -1, length = blocks[loc].length + blocks[loc + 1].length)
        blocks.pop(loc + 1)
    if loc > 0 and blocks[loc - 1].id == -1:
        blocks[loc - 1] = Block(id = -1, length = blocks[loc - 1].length + blocks[loc].length)
        blocks.pop(loc)

def part2(data):
    sorted = data.blocks2
    start = data.lastFile

    # Move each file to the first available position in the disk, starting with the file at the end of the disk
    for id in range(start, 0, -1):
        # find the next file to move
        oldPos, file = find(id, sorted)

        # find the next available position to move the file to
        for i, block in enumerate(sorted):
            if i >= oldPos:
                break
            
            # If the block is free space and is large enough to fit the file, move the file to the block
            if block.id == -1 and block.length >= file.length:
                diff = block.length - file.length
                sorted[oldPos] = Block(id = -1, length = file.length)
                sorted[i] = file
                consolidate(oldPos, sorted) # consolidate the free space around the file's old position

                # If the free space is larger than the file
                if diff > 0:
                    sorted.insert(i + 1, Block(id = -1, length = diff)) # insert the remaining free space after the file
                    consolidate(i + 1, sorted) # consolidate the free space with any surrounding free space

                break

    # Calculate the checksum of the sorted blocks and print the result
    return calcChecksum2(sorted)

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
    run(samp)
run(data)