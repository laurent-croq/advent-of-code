#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def solve(numbers, max_turn):
    previous = {}
    last_seen = {}
    for i,n in enumerate(numbers):
        last_seen[n] = i+1

    last_one = numbers[-1]
    turn = len(numbers)

    while turn < max_turn:
        next_one = last_seen[last_one]-previous[last_one] if last_one in previous else 0
        if next_one in last_seen:
            previous[next_one] = last_seen[next_one]

        turn += 1
        last_seen[next_one] = turn
        last_one = next_one
    
    return(last_one)

def puzzles(input_lines, **extra_args):
    numbers = [ int(n) for n in input_lines[0].split(',') ]

    yield(solve(numbers, 2020))
    yield(solve(numbers, 30000000))

aoc.run(puzzles)
