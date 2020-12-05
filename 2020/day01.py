#!/usr/bin/python3

import aoc
puzzle_numbers = [ int(n) for n in aoc.read_puzzle_input() ]

for i, n in enumerate(puzzle_numbers):
    if 2020-n in puzzle_numbers[i+1:]:
        print("answer1 = %d" % (n*(2020-n)))

for i, n in enumerate(puzzle_numbers):
    for j, m in enumerate(puzzle_numbers[i+1:]):
        if 2020-n-m in puzzle_numbers[j+1:]:
            print("answer2 = %d" % (n*m*(2020-n-m)))

