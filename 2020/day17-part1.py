#!/usr/bin/python3

import aoc

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

def next_grid(grid):
    extend_grid(grid)

    new_grid = copy.deepcopy(grid)
    for z,y,x in [ [z,y,x] for z in range(1, len(grid)-1) for y in range(1, len(grid[z])-1) for x in range(1, len(grid[z][y])-1) ]:
        total_neighbors = sum(grid[z+dz][y+dy][x+dx] for dz,dy,dx in [ [dz,dy,dx] for dz in range(-1, 2) for dy in range(-1, 2) for dx in range(-1, 2) if not(dx==dy==dz==0)])
        if new_grid[z][y][x]:
            new_grid[z][y][x] = True if total_neighbors in [2,3] else False
        else:
            new_grid[z][y][x] = True if total_neighbors == 3 else False
    return(new_grid)

def puzzles(input_lines):
    grid = [ [] ]
    for line in input_lines:
        grid[0].append([ i == '#' for i in line ])

    extend_grid(grid)
    for _ in range(6):
        grid = next_grid(grid)

    yield(sum(grid[z][y][x] for z,y,x in [ [z,y,x] for z in range(len(grid)) for y in range(len(grid[z])) for x in range(len(grid[z][y])) ]))
    yield(None)

aoc.run(puzzles)
