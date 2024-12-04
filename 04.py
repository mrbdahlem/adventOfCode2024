import helper

day = int(__file__.split("\\")[-1].split(".")[0])
print ("Day", day)

data = helper.load_data(day)
# data = helper.load_data("04-samp")
lines = data.splitlines()
search = [list(line) for line in lines]

def countStrings(row, col, search, string):
    """ Look in the word search, starting at the given row and column, for the given string
    in all 8 directions. Return the number of times the string is found. """
    count = 0

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            if getString(row, col, search, dx, dy, len(string)) == string:
                count+=1

    return count

def getString(row, col, search, dx, dy, length):
    """ Get a string from the word search starting at the given row and column, 
    and moving in the given direction for the given length. """
    string = ""
    y = row
    x = col
    
    while y >= 0 and y < len(search) and x >= 0 and x < len(search[y]) and len(string) < length:
        string += search[x][y]
        x += dx
        y += dy

    return string

def getX(row, col, search, string):
    """ Check if the given string is found in the word search, centered around the given row and column,
    in two opposite directions. """
    count = 0
    for (dx, dy) in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        if (getString(row - (dy * (len(string) // 2)), col - (dx * (len(string) // 2)),
                      search, dx, dy, len(string)) == string):
            count += 1
    
    return count == 2

# Count the number of times the string "XMAS" appears in the word search
count = 0
for row in range(len(search)):
    for col in range(len(search[row])):
        count += countStrings(row, col, search, "XMAS")

print("Part 1: ", count)

# Count the number of times the string "MAS" appears in the word search as an X
count = 0
for row in range(len(search)):
    for col in range(len(search[row])):
        if (getX(row, col, search, "MAS")):
            count += 1


print("Part 2: ", count)