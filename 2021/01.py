#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def solve_puzzle(input_lines, **extra_args):
    measurements = [ int(n) for n in input_lines ]
    answer1 = 0
    answer2 = 0
    for i in range(1, len(measurements)):
        answer1 += (measurements[i]>measurements[i-1])
        if i<len(measurements)-2:
            answer2 += (sum(measurements[i:i+3])>sum(measurements[i-1:i+2]))

    yield(answer1)
    yield(answer2)

aoc.run(solve_puzzle, samples = { 1: [ 7, 5 ] })
