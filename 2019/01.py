#!/usr/bin/python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def total_required_fuel(n):
    if n<=0:
        return(0)

    f = max(0,n//3-2)
    return(f+total_required_fuel(f))

def puzzles(input_lines, **extra_args):
    answer1 = 0
    answer2 = 0
    for n in [ int(n) for n in input_lines ]:
        answer1 += n//3-2
        answer2 += total_required_fuel(n)
    
    yield(answer1)
    yield(answer2)

aoc.run(puzzles)
