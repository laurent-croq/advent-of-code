#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc, heapq

def lowest_risk(cavern):
    costs = [ [None] * len(cavern[0]) for _ in range(len(cavern)) ]

    positions = []
    target = (len(cavern[0])-1, len(cavern)-1)

    heapq.heappush(positions, (0, (0,0)))
    while len(positions)>0:
        risk_level, pos = heapq.heappop(positions)
        if pos == target:
            return risk_level

        if costs[pos[1]][pos[0]] is None or costs[pos[1]][pos[0]] > risk_level:
            costs[pos[1]][pos[0]] = risk_level

            for dx,dy in [ [dx,dy] for dx,dy in [ [-1,0], [1,0], [0,-1], [0,1] ] if pos[0]+dx>=0 and pos[1]+dy>=0 and pos[0]+dx<len(cavern[0]) and pos[1]+dy<len(cavern) ]:
                new_pos = (pos[0]+dx, pos[1]+dy)
                new_cost = risk_level + cavern[new_pos[1]][new_pos[0]]
                    
                if costs[new_pos[1]][new_pos[0]] is None or costs[new_pos[1]][new_pos[0]] > new_cost:
                    heapq.heappush(positions, (new_cost, new_pos))

    return None

def solve_puzzle(input_lines, **extra_args):

    cavern = [ [int(c) for c in line ] for line in input_lines ]

    yield lowest_risk(cavern)

    for y,line in enumerate(cavern):
        line = line[:]
        for i in range(1,5):
            cavern[y].extend([ ((v-1+i)%9)+1 for v in line ])

    initial_size = len(cavern)
    for i in range(1,5):
        for y in range(initial_size):
            cavern.append([ ((v-1+i)%9)+1 for v in cavern[y] ])

    yield lowest_risk(cavern)

aoc.run(solve_puzzle, samples = { 1:[40,315] })
