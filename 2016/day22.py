#!/usr/bin/python3

import aoc

from itertools import combinations,filterfalse
import re
from copy import deepcopy
from heapq import heappop, heappush

def are_nodes_viable(nodeA, nodeB, used, size):
    return(used[nodeA[0]][nodeA[1]] <= (size[nodeB[0]][nodeB[1]]-used[nodeB[0]][nodeB[1]]) and used[nodeA[0]][nodeA[1]]>0) or (used[nodeB[0]][nodeB[1]] <= (size[nodeA[0]][nodeA[1]]-used[nodeA[0]][nodeA[1]]) and used[nodeB[0]][nodeB[1]]>0)

def are_nodes_adjacent(nodeA, nodeB):
    return(nodeA != nodeB and abs(nodeA[0]-nodeB[0])+abs(nodeA[1]-nodeB[1])<2)

def puzzles(input_lines, **extra_args):
    max_x = int(extra_args.get("max_x", 36))
    max_y = int(extra_args.get("max_y", 30))
    used = [ [0] * max_x for _ in range(max_y) ]
    size = [ [0] * max_x for _ in range(max_y) ]
    for line in input_lines:
        m = re.match(r'/dev/grid/node-x(\d+)-y(\d+) +(\d+)T +(\d+)T +(\d+)T', line)
        if m is None:
            continue
        used[int(m.group(2))][int(m.group(1))] = int(m.group(4))
        size[int(m.group(2))][int(m.group(1))] = int(m.group(3))

    all_nodes = [ (y,x) for x in range(max_x) for y in range(max_y) ]
    total_viable = 0
    for nodeA,nodeB in combinations(all_nodes, 2):
        total_viable += are_nodes_viable(nodeA, nodeB, used, size)

    yield(total_viable)

    if True:
        print("Size:")
        for y in range(len(used)):
            print(" ".join("%3d" % a for a in size[y]))

        print("Used:")
        for y in range(len(used)):
            print(" ".join("%3d" % u for u in used[y]))

    states = []
    pos = (0, len(size[0])-1)
    total_states = 0
    heappush(states, (0, pos, 0, used))
    history = []
    min_steps = 0
    while True:
        if len(states) == 0:
            print("Not found!")
            exit(1)
        steps, pos, _, used = heappop(states)
        print("%3d states to explore, min_steps=%d" % (len(states), min_steps))
        if steps > min_steps:
            min_steps = steps
        if used in history:
            continue
        history.append(used)
        if pos == (0,0):
            break

        total_added = 0
        for nodeA,nodeB in filterfalse(lambda nodes: not(are_nodes_adjacent(nodes[0], nodes[1]) and are_nodes_viable(nodes[0], nodes[1], used, size)), combinations(all_nodes, 2)):
            #print("Checking %s and %s" % (nodeA, nodeB))
            if used[nodeA[0]][nodeA[1]]>0 and used[nodeA[0]][nodeA[1]] <= (size[nodeB[0]][nodeB[1]]-used[nodeB[0]][nodeB[1]]):
                total_added += 1
                #print("Moving %s to %s" % (nodeA, nodeB))
                new_used = deepcopy(used)
                new_used[nodeB[0]][nodeB[1]] += used[nodeA[0]][nodeA[1]]
                new_used[nodeA[0]][nodeA[1]] = 0
                total_states += 1
                heappush(states, (steps+1, pos if pos!=nodeA else nodeB, total_states, new_used))

            if used[nodeB[0]][nodeB[1]]>0 and used[nodeB[0]][nodeB[1]] <= (size[nodeA[0]][nodeA[1]]-used[nodeA[0]][nodeA[1]]):
                total_added += 1
                #print("Moving %s to %s" % (nodeB, nodeA))
                new_used = deepcopy(used)
                new_used[nodeA[0]][nodeA[1]] += used[nodeB[0]][nodeB[1]]
                new_used[nodeB[0]][nodeB[1]] = 0
                total_states += 1
                heappush(states, (steps+1, pos if pos!=nodeB else nodeA, total_states, new_used))
        #print("Added %d" % total_added)

    yield(steps)

aoc.run(puzzles)