#!/usr/bin/python3

import aoc
puzzle_lines = aoc.load_puzzle_input()

grid = []
for line in puzzle_lines:
    grid.append( [ i == '#' for i in line ] )

import copy
def extend_grid(grid):
    if type(grid[0]) == bool:
        grid.insert(0, False)
        grid.append(False)
    else:
        for line in grid:
            extend_grid(line)

        empty_line = [ copy.deepcopy(grid[0][0]) for _ in range(len(line)) ]
        grid.insert(0, empty_line)
        grid.append(copy.deepcopy(empty_line))

def neighbors(grid, v, sumnz=0):
    if type(grid) == bool:
        return(0 if sumnz == 0 else int(grid))
    else:
        total = 0
        for delta in range(-1, 2):
            total += neighbors(grid[v[0]+delta], v[1:], sumnz+(delta!=0))
        return(total)

def next_grid(dimensions, grid, v, new_grid):
    if len(v) == dimensions:
        total = neighbors(grid, v)
        for i in v[:-1]:
            new_grid = new_grid[i]
            grid = grid[i]
        if grid[v[-1]]:
            new_grid[v[-1]] = True if total in [2,3] else False
        else:
            new_grid[v[-1]] = True if total == 3 else False
    else:
        nextg = grid
        for i in v:
            nextg = nextg[i]
        for i in range(1, len(nextg)-1):
            next_grid(dimensions, grid, v+[i], new_grid)

def sum_grid(grid):
    return(int(grid) if type(grid) == bool else sum([ sum_grid(g) for g in grid ]))

def answer(grid, dimensions):
    for _ in range(dimensions-2):
        grid = [ grid ]

    extend_grid(grid)
    for _ in range(6):
        extend_grid(grid)

        new_grid = copy.deepcopy(grid)
        next_grid(dimensions, grid, [], new_grid)
        grid = new_grid
    
    return(sum_grid(new_grid))

print("answer1 = %d" % answer(grid[:], 3))
print("answer2 = %d" % answer(grid[:], 4))
