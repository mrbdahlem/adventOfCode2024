from types import SimpleNamespace
import helper
import os

from copy import copy, deepcopy
from collections import defaultdict, deque
import re
from functools import cache
from PIL import Image, ImageDraw
import asyncio
import heapq

@helper.timeit
def parse(data):
    parsed = SimpleNamespace()
    parsed.numbers = list(map(int, data.splitlines()))
    return parsed

################################

def mixPrune(num, num2):
    return (num ^ num2) % 16777216

def secretRound(num):
    num = mixPrune(num, num * 64)
    num = mixPrune(num, num // 32)
    num = mixPrune(num, num * 2048)
    return num


def findSecretN(num, rounds):
    for _ in range(rounds):
        num = secretRound(num)

    return num

@helper.timeit
def part1(data):
    total = 0
    for n in data.numbers:
        total += findSecretN(n, 2000)
    return total

################################

@helper.timeit
def part2(data):

    totalMap = defaultdict(lambda: 0)

    for num in data.numbers:
        deltaMap = dict()
        deltas = deque()
        last = 0
        for i in range(2000):
            num = secretRound(num)
            amt = num % 10
            delta = amt - last

            if i > 0:
                deltas.append(delta)
            if len(deltas) > 4:
                deltas.popleft()

            if len(deltas) == 4:
                deltaTuples = tuple(deltas)
                if not deltaTuples in deltaMap:
                    deltaMap[tuple(deltas)] = amt

            last = amt

        for delta, amt in deltaMap.items():
                totalMap[delta] += amt

    return max(totalMap.values())

################################

def run(data, stage):
    """
    Run both parts of the day
    """
    parsed = parse(data)
    parsed.stage = stage
    print("-" * 24)
    
    # Solve the first part
    print("Part 1: {\033[0;41m\033[1;97m " + str(part1(parsed)) + " \033[0m}", part1Wrong[stage])

    # Solve the second part
    print("Part 2: {\033[0;42m\033[1;97m " + str(part2(parsed)) + " \033[0m}", part2Wrong[stage])

################################

async def main():
    sep = "~" * 56
    print(sep)

    # Get the day number from this file's name
    day = int(__file__.split(os.sep)[-1].split(".")[0])
    print (f"{f' Day {day} ':*^{len(sep)}}")
    print(sep)

    # load a sample data file for this day, if it exists
    if helper.exists(f"{day:02}-samp"):
        print(f"{' Sample Data ':-^{len(sep)}}")
        data = helper.load_data(f"{day:02}-samp")
        if data:
            run(data, 'samp')
    
    # load the actual data for this day
    print(f"{' Actual Data ':-^{len(sep)}}")

    data = helper.load_data(day)
    run(data, 'full')
    print(sep)

part1Wrong = {
    "samp": [],
    "full": []
}

part2Wrong = {
    "samp": [],
    "full": []
}


asyncio.run(main())