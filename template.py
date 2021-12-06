#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def solve_puzzle(input_lines, **extra_args):
    answer1 = None
    answer2 = None

    #for n in [ int(n) for n in input_lines ]:
    #for line in input_lines:
    
    yield answer1
    yield answer2

aoc.run(solve_puzzle, samples = {} )
