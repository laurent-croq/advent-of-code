#!/usr/bin/python3

import aoc
puzzle_lines = aoc.load_puzzle_input()

def count_trees(slope):
    pos = [0, 0]
    total_trees = 0
    while pos[1] < len(puzzle_lines):
        pos[0] %= len(puzzle_lines[0])
        if puzzle_lines[pos[1]][pos[0]] == '#':
            total_trees += 1

        pos[0] += slope[0]
        pos[1] += slope[1]

    return(total_trees)

import math

print("answer1 = %d" % count_trees([3, 1]))
print("answer2 = %d" % math.prod([ count_trees(slope) for slope in [ [1,1], [3,1], [5,1], [7,1], [1,2] ] ]))
