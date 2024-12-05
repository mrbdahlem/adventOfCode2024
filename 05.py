import helper
from functools import cmp_to_key

day = int(__file__.split("\\")[-1].split(".")[0])
print ("Day", day)

data = helper.load_data(day)
# data = helper.load_data(f"{day:02}-samp")

# Split the data into the rule specification and the updates
data = data.split("\n\n")
ruleSpec = data[0].splitlines()
updates = data[1].splitlines()

# Create a dictionary of rules - a page and the list of pages it must precede
mustPrecede = dict()
for spec in ruleSpec:
    # split the rule into a page and the page it must precede
    pages = spec.split("|")
    
    # add/update the rule in the dictionary
    rule = mustPrecede.get(pages[0], [])
    rule.append(pages[1])
    mustPrecede[pages[0]] = rule

# Solve Part 1

# calculate the total of the middle page numbers in all of the valid updates
totalMids = 0

bad = [] # Bad updates for part 2

# find all of the valid updates
for update in updates:
    pages = update.split(",") # split the update into a list of page numbers

    # ensure that no page occurs before a page it must precede
    invalid = False
    for i in range(len(pages)):
        # get the list of pages that the current page must preceed
        rule = mustPrecede.get(pages[i], [])

        # check if any of the pages in the update before the current page are in the list
        for j in range(i):
            if pages[j] in rule:
                # if so, the update is invalid
                invalid = True
                break

        # if the update is invalid, stop checking and add the update to the bad list for part 2
        if (invalid):
            bad.append(update)
            break

    # if the update is valid, add the middle page number to the total
    if not invalid:
        totalMids += int(pages[len(pages) // 2])

print("Part 1: ", totalMids)

# Solve Part 2

def checkProceeds(a, b):
    """
    Compare two pages to determine if one must precede the other based on the rules given
    """

    # get the list of pages that the first page must preceed
    rule = mustPrecede.get(a, [])

    # if the second page is in the list, the first page must precede the second
    if b in rule:
        return 1

    # get the list of pages that the second page must preceed
    rule = mustPrecede.get(b, [])

    # if the first page is in the list, the second page must precede the first
    if a in rule:
        return -1

    # if neither page must precede the other, return 0
    return 0

# calculate the total of the middle page numbers of all of the bad updates,
# after putting the pages in the correct order
totalBadMids = 0
for update in bad:
    # split the update into a list of page numbers
    pages = update.split(",")

    # sort the pages based on the rules given
    pages.sort(key=cmp_to_key(checkProceeds))

    # add the middle page number to the running total
    totalBadMids += int(pages[len(pages) // 2])

print("Part 2: ", totalBadMids)