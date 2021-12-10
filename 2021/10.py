#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def costs(line):
    chunk_pair = dict(zip("([{<", ")]}>"))
    chunk_cost = dict(zip("([{<)]}>", [1,2,3,4,3,57,1197,25137]))

    stack = ""

    for c in line:
        if c in chunk_pair:
            stack += c
        elif c == chunk_pair[stack[-1]]:
            stack = stack[:-1]
        else:
            return chunk_cost[c], None

    cost = 0
    for c in stack[::-1]:
        cost = cost*5 + chunk_cost[c]

    return None, cost
        
def solve_puzzle(input_lines, **extra_args):
    answer1 = 0
    answer2 = []

    for line in input_lines:
        resp1, resp2 = costs(line)
        if resp1 is not None:
            answer1 += resp1
        else:
            answer2.append(resp2)
    
    yield answer1
    yield sorted(answer2)[len(answer2)//2]

aoc.run(solve_puzzle, samples = { 1: [ 26397, 288957 ] })
