#!/usr/bin/python3

import aoc

from functools import reduce
from operator import xor

def knot_hash(numbers, lengths, count=1):
    skip = begin = 0
    for length in lengths * count:
        numbers = numbers[:length][::-1] + numbers[length:]
        numbers = numbers[(length+skip)%len(numbers):] + numbers[:(length+skip)%len(numbers)]
        begin = (begin-skip-length)%len(numbers)
        skip += 1
    return(numbers[begin:] + numbers[:begin])

def clear_grid(grid, y, x):
    if not(y in range(128) and x in range(128) and grid[y][x]):
        return
    
    grid[y][x] = False
    clear_grid(grid, y+1, x)
    clear_grid(grid, y-1, x)
    clear_grid(grid, y, x+1)
    clear_grid(grid, y, x-1)

def puzzles(input_lines, **extra_args):
    grid = []
    for i in range(128):
        lengths = [ ord(c) for c in input_lines[0]+"-"+str(i) ] + [ 17, 31, 73, 47, 23 ]
        numbers = knot_hash(list(range(int(extra_args.get("n", 256)))), lengths, 64)
        grid.append(list(c=="1" for c in "".join("%8s" % bin(i)[2:] for i in [ reduce(xor, block) for block in [ numbers[i:i+16] for i in range(0,256,16) ] ])))

    yield(sum(l.count(True) for l in grid))

    answer_part2 = 0
    for y in range(len(grid)):
        try:
            while True:
                x = grid[y].index(True)
                clear_grid(grid, y, x)
                answer_part2 += 1
        except:
            pass

    yield(answer_part2)

aoc.run(puzzles)