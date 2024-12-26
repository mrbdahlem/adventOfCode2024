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
    
    parts = data.strip().split("\n\n")

    parsed.initial = dict()
    for line in parts[0].split("\n"):
        k,v = line.split(": ")
        parsed.initial[k] = int(v)

    parsed.wires = copy(parsed.initial)
    parsed.gates = []
    for line in parts[1].split("\n"):
        gateInfo = line.split(" ")
        gate = Gate(gateInfo[1], gateInfo[0], gateInfo[2], gateInfo[-1])
        parsed.gates.append(gate)

        for w in [gateInfo[0], gateInfo[2], gateInfo[-1]]:
            if not w in parsed.wires:
                parsed.wires[w] = None

        # print(gate)

    return parsed

class Gate:
    def __init__(self, type, input0, input1, output):
        self.type = type
        self.input0 = input0
        self.input1 = input1
        self.output = output

    def __repr__(self):
        return f"{self.type} {self.input0} {self.input1} -> {self.output}"

################################

def runGates(gates, wires, initial):
    setWires = copy(initial)

    while len(setWires) < len(wires):
        for gate in gates:
            if gate.input0 in setWires and gate.input1 in setWires:
                if gate.type == "AND":
                    setWires[gate.output] = setWires[gate.input0] & setWires[gate.input1]
                elif gate.type == "OR":
                    setWires[gate.output] = setWires[gate.input0] | setWires[gate.input1]
                elif gate.type == "XOR":
                    setWires[gate.output] = setWires[gate.input0] ^ setWires[gate.input1]

    return setWires

@helper.timeit
def part1(data):

    setWires = runGates(data.gates, copy(data.wires), data.initial)
                
    zWires = dict()
    for w,v in setWires.items():
        if w.startswith("z"):
            zWires[w] = v

    val = 0
    for w in sorted(zWires.keys(), reverse=True):
        val = (val << 1) + zWires[w]
        
    return val

################################

@helper.timeit
def part2(data):

    for gate in sorted(data.gates, key=lambda x: x.input0):
        print(gate)
    return 0

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
    "full": [(0, 'low'), (0, 'high')]
}


asyncio.run(main())