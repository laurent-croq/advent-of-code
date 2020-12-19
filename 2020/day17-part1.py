#!/usr/bin/python3

import os, sys
sys.path.insert(1, os.getcwd()+"/..")
import aoc
puzzle_lines = aoc.load_puzzle_input()

grid = [ [] ]

for line in puzzle_lines:
    grid[0].append( [ i == '#' for i in line ] )

import copy
def extend_grid(grid):

        for layer in grid:
            for line in layer:
                line.insert(0, False)
                line.append(False)

            empty_line = [ False for _ in range(len(line)) ]
            layer.insert(0, empty_line)
            layer.append(copy.deepcopy(empty_line))

        empty_layer = [ copy.deepcopy(empty_line) for _ in range(len(layer)) ]
        grid.insert(0, empty_layer)
        grid.append(copy.deepcopy(empty_layer))

def dump_grid(grid):
    for z, layer in enumerate(grid):
        print("z=%d" % z)
        for y, line in enumerate(layer):
            print("%s (y=%d)" % ("".join([ "#" if p else "." for p in line ]), y))
        print

def neighors(grid, x, y, z):
    total = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                if dx==dy==dz==0:
                    continue
                else:
                    total+=grid[z+dx][y+dy][x+dz]
    return(total)

def next_grid(grid):
    extend_grid(grid)

    new_grid = copy.deepcopy(grid)

    for z in range(1, len(grid)-1):
        for y in range(1, len(grid[z])-1):
            for x in range(1, len(grid[z][y])-1):
                total = neighors(grid, x, y, z)
                if new_grid[z][y][x]:
                    new_grid[z][y][x] = True if total in [2,3] else False
                else:
                    new_grid[z][y][x] = True if total == 3 else False
    return(new_grid)

def sum_grid(grid):
    total = 0
    for z in range(len(grid)):
        for y in range(len(grid[z])):
            for x in range(len(grid[z][y])):
                total += grid[z][y][x]
    return(total)


extend_grid(grid)
for _ in range(6):
    new_grid = next_grid(grid)
    grid = new_grid

print("answer1 = %d" % sum_grid(new_grid))
