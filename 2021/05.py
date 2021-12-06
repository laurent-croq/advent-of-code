#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def solve_puzzle(input_lines, **extra_args):
    answer1 = 0
    answer2 = None

    lines = []

    size_grid = 1000
    for c1,c2 in [ line.split(" -> ") for line in input_lines ]:
        lines.append(list(map(int,c1.split(","))) + list(map(int,c2.split(","))))

    grid = [ [0] * size_grid for _ in range(size_grid) ]

    for x0,y0,x1,y1 in [ line for line in lines ]:
        if x0 == x1:
            for y in range(min(y0,y1), max(y0,y1)+1):
                grid[y][x0] += 1
        elif y0 == y1:
            for x in range(min(x0,x1), max(x0,x1)+1):
                grid[y0][x] += 1
        else:
            x = x0
            y = y0
            for _ in range(min(y0,y1), max(y0,y1)+1):
                grid[y][x] += 1
                x += (1 if x1>x0 else -1)
                y += (1 if y1>y0 else -1)

    for line in grid:
        for v in line:
            if v>=2:
                answer1+=1
    yield answer1
    yield answer2

aoc.run(solve_puzzle, samples = {} )
