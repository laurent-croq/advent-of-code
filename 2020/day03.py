#!/usr/bin/python3

import aoc

import math

def count_trees(input_lines, slope):
    x = y = 0
    total_trees = 0
    while y < len(input_lines):
        x %= len(input_lines[0])
        total_trees += input_lines[y][x] == '#'
        x += slope[0]
        y += slope[1]

    return(total_trees)

def puzzles(input_lines, **extra_args):
    yield(count_trees(input_lines, [3, 1]))
    yield(math.prod([ count_trees(input_lines, slope) for slope in [ [1,1], [3,1], [5,1], [7,1], [1,2] ] ]))

aoc.run(puzzles, samples = { 1: [ 7, 336 ] })