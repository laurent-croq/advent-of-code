#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import itertools

def is_valid_triangle(triangle):
    for s1,s2,s3 in itertools.permutations(triangle):
        if s1 >= s2+s3:
            return(False)
    return(True)
    
def puzzles(input_lines, **extra_args):
    input_numbers = [ int(n) for n in " ".join(input_lines).split() ]

    total_valid = 0
    for triangle in [ input_numbers[i:i+3] for i in range(0, len(input_numbers), 3) ]:
        total_valid += is_valid_triangle(triangle)
    yield(total_valid)

    total_valid = 0
    for group in [ input_numbers[i:i+9] for i in range(0, len(input_numbers), 9) ]:
        for i in range(3):
            total_valid += is_valid_triangle([ group[i], group[i+3], group[i+6]])
    yield(total_valid)

aoc.run(puzzles)
