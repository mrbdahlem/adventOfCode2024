import datetime
import os
import subprocess

# get the current day of the month
day = datetime.datetime.now().day

scriptDay = -1

while scriptDay < 1 or scriptDay > 25:
    if datetime.datetime.now().month == 12:
        print("Today is day", day)
        chosen = input(f"What day (1-{day}) would you like to run (enter for today)? ")
        if chosen == "":
            chosen = day
    else:
        chosen = input("What day would you like to run? ")

    try:
        scriptDay = int(chosen)
    except:
        scriptDay = -1

script = str(scriptDay).zfill(2) + ".py"

if os.path.exists(script):
    subprocess.run(["python", script])
else:
    print("Day", scriptDay, "does not exist, creating it now.")
    with open("00.template", "r") as template:
        contents = template.read()
    with open(script, "w") as newScript:
        newScript.write(contents)


