from types import SimpleNamespace
import helper
import os

from copy import copy, deepcopy
from collections import defaultdict
import re
from functools import cache
from PIL import Image, ImageDraw
import asyncio
import heapq

@helper.timeit
def parse(data):
    parsed = SimpleNamespace()
    parts = data.strip().split("\n\n")

    regs = parts[0].split("\n")
    parsed.regs = dict()
    for reg in regs:
        regparts = reg.split(": ")
        parsed.regs[list(regparts[0])[-1]] = int(regparts[1])

    parsed.instructions = [int(x) for x in parts[1].split(': ')[1].split(",")] 

    return parsed

################################
class Device:
    """
    A representation of a 3-bit intcode device
    """
    def __init__(self):
        self.regs = dict()
        self.ip = 0
        self.instructions = []
        self.out = ''

    def loadInstructions(self, instructions):
        """
        Load the instructions into the device

        Args:
            instructions (list): The list of 3-bit instructions to load
        """
        self.instructions = instructions

    def getOut(self):
        """
        Get the output from the device
        """
        return self.out
    
    def reset(self):
        """
        Reset the device to restart the already loaded instructions
        """
        self.ip = 0
        self.out = ''

    def setReg(self, reg, val):
        """
        Set the value of a register
        """
        self.regs[reg] = val

    def run(self):
        """
        Run the loaded instructions
        """
        while self.ip < len(self.instructions):
            self._runInstruction(self.instructions[self.ip], self.instructions[self.ip + 1])
            self.ip += 2

    def _runInstruction(self, instruction, data):
        if instruction == 0: # adv
            val = self.regs['A'] // 2**(self.combo(data))
            self.regs['A'] = val

        elif instruction == 1: # bxl
            val = self.regs['B'] ^ data
            self.regs['B'] = val

        elif instruction == 2: # bst
            val = self.combo(data) % 8
            self.regs['B'] = val

        elif instruction == 3: # jnz
            if self.regs['A'] != 0:
                self.ip = data - 2

        elif instruction == 4: # bxc
            val = self.regs['B'] ^ self.regs['C']
            self.regs['B'] = val

        elif instruction == 5: # out
            if self.out:
                self.out += ','

            self.out += str(self.combo(data) % 8)

        elif instruction == 6: # bdv
            val = self.regs['A'] // 2**(self.combo(data))
            self.regs['B'] = val

        elif instruction == 7: # cdv
            val = self.regs['A'] // 2**(self.combo(data))
            self.regs['C'] = val

    def combo(self, data):
        """
        Get the value of the combo operand
        """
        if data >= 0 and data <= 3:
            return data
        elif data == 4:
            return self.regs['A']
        elif data == 5:
            return self.regs['B']
        elif data == 6:
            return self.regs['C']
        elif data == 7:
            print("Error: invalid combo operand 7")

@helper.timeit
def part1(data):
    """
    Solve part 1 - run the device and return the output
    """
    comp = Device()
    comp.setReg('A', data.regs['A'])
    comp.setReg('B', data.regs['B'])
    comp.setReg('C', data.regs['C'])
    comp.loadInstructions(data.instructions)
    comp.reset()
    comp.run()

    return comp.getOut()

################################

def findMatch(soFar, prg, comp):
    """
    Find the A register value that causes the device to output a match for the given program
    """
    global runs

    # Make room for the next 3 bits in the previous A register value
    prevA = soFar << 3
    
    # Try all possible values for the next 3 bits
    for i in range(8):
        nextA = prevA + i
        # Set the A register to the previous value with the next 3 bits
        comp.setReg('A', nextA)
        comp.setReg('B', 0)
        comp.setReg('C', 0)
        comp.reset()

        # Run the device with the current A input
        comp.run()

        # If the output matches the program, return the A register value that caused it
        if prg == comp.getOut():
            return nextA
        
        # If the output matches the end of the program, try to find the next 3 bits of the input
        if (prg.endswith(comp.getOut())):
            a = findMatch(nextA, prg, comp)
            if a is not None:
                return a
            
    return None

@helper.timeit
def part2(data):
    prog = ','.join([str(x) for x in data.instructions])

    comp = Device()
    comp.setReg('A', 0)
    comp.setReg('B', 0)
    comp.setReg('C', 0)
    comp.loadInstructions(data.instructions)
    
    return findMatch(0, prog, comp)

################################

def run(data, stage):
    """
    Run both parts of the day
    """
    parsed = parse(data)
    parsed.stage = stage
    print("-" * 24)
    
    # Solve the first part
    print("Part 1: {\033[0;41m\033[1;97m " + str(part1(parsed)) + " \033[0m}")

    # Solve the second part
    print("Part 2: {\033[0;42m\033[1;97m " + str(part2(parsed)) + " \033[0m}")

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
        # if data:
        #     run(data, 'samp')
    
    # load the actual data for this day
    print(f"{' Actual Data ':-^{len(sep)}}")

    data = helper.load_data(day)
    run(data, 'full')
    print(sep)

asyncio.run(main())