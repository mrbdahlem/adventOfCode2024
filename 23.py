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
    parsed.connections = defaultdict(lambda: set())

    # Parse the data into a dictionary of sets of connected vertices
    for line in data.splitlines():
        [a,b] = line.split('-')
        parsed.connections[a].add(b)
        parsed.connections[b].add(a)

    return parsed

################################

@helper.timeit
def part1(data):

    # Find all triplets of vertices that are connected to each other and include at least one starting with 't'
    triplets = set()
    for a in data.connections:
        if a.startswith('t'):
            for b in data.connections[a]:
                for c in data.connections[b]:
                    if c != a and c in data.connections[a]:
                        triplets.add(tuple(sorted([a,b,c])))

    return len(triplets)

################################

def BronKerbosch(clique, candidates, excluded, connections, cliques):
    """
    Bron-Kerbosch algorithm for finding all maximal cliques in a graph
    """
    # If there are no more candidates or excluded vertices, we have a maximal clique
    if len(candidates) == 0 and len(excluded) == 0:
        if len(clique) > 2:
            cliques.append(sorted(clique))
        return
    
    # For each vertex in the candidates set
    for v in copy(candidates):
        # Add the vertex to the clique
        newClique = clique.union(set([v]))

        # Find the new candidates and excluded vertices by limiting them to the vertices connected to the current vertex
        newCandidates = candidates.intersection(connections[v])
        newExcluded = excluded.intersection(connections[v])

        # Recursively call the function with the new clique, candidates, and excluded vertices
        BronKerbosch(newClique, newCandidates, newExcluded, connections, cliques)
        
        # Remove the vertex from the candidates set and add it to the excluded set
        candidates.remove(v)
        excluded.add(v)

@helper.timeit
def part2(data):

    # Find all maximal cliques in the graph
    cliques = []
    BronKerbosch(set([]), set(data.connections.keys()), set([]), data.connections, cliques)
    
    # Find the largest clique
    maxClique = ','.join(sorted(max(cliques, key=len)))

    return maxClique
    

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