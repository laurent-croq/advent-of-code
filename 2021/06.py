#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def solve_puzzle(input_lines, **extra_args):

    fishes = [0]*9

    for n in [ int(n) for n in input_lines[0].split(",") ]:
        fishes[n] += 1

    for day in range(256):
        fishes = fishes[1:] + [fishes[0]]
        fishes[6] += fishes[8]

        if day == 79:
            yield sum(fishes)

    yield sum(fishes)

aoc.run(solve_puzzle, samples = { 1: [ 5934, 26984457539 ] } )
