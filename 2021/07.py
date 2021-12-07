#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def solve_puzzle(input_lines, **extra_args):
    answer1 = None
    answer2 = None

    horizontals = [ int(n) for n in input_lines[0].split(",") ]
    
    costs_answer1 = [0] * max(horizontals)
    costs_answer2 = [0] * max(horizontals)

    for i in range(max(horizontals)):
        for j in horizontals:
            costs_answer1[i] += abs(i-j)
            costs_answer2[i] += abs(i-j) * (abs(i-j)+1) // 2

        answer1 = costs_answer1[i] if answer1 is None or answer1>costs_answer1[i] else answer1
        answer2 = costs_answer2[i] if answer2 is None or answer2>costs_answer2[i] else answer2

    yield answer1
    yield answer2

aoc.run(solve_puzzle, samples = { 1: [ 37, 168 ]} )
