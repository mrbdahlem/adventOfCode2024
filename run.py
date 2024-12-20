import datetime
import os
import subprocess
import helper

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

script = f"{scriptDay:02}.py"

if os.path.exists(script):
    subprocess.run(["python", script])
else:
    print("Day", scriptDay, "does not exist, creating it now.")
    with open("00.template", "r") as template:
        contents = template.read()
    with open(script, "w") as newScript:
        newScript.write(contents)
    print(f"{scriptDay:02}.py created. Downloading input to data/{scriptDay:02}.txt.")
    helper.load_data(scriptDay)
    sampleFile = f"data/{scriptDay:02}-samp.txt"
    print(f"Creating sample input file {sampleFile}.")
    with open(sampleFile, "w") as sample:
        sample.write("")


