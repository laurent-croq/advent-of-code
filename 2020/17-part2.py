#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import copy

def extend_grid(grid):
    for cube in grid:
        for layer in cube:
            for line in layer:
                line.insert(0, False)
                line.append(False)

            empty_line = [ False for _ in range(len(line)) ]
            layer.insert(0, empty_line)
            layer.append(copy.deepcopy(empty_line))

        empty_layer = [ copy.deepcopy(empty_line) for _ in range(len(layer)) ]
        cube.insert(0, empty_layer)
        cube.append(copy.deepcopy(empty_layer))

    empty_cube = [ copy.deepcopy(empty_layer) for _ in range(len(cube)) ]
    grid.insert(0, empty_cube)
    grid.append(copy.deepcopy(empty_cube))

def next_grid(grid):
    extend_grid(grid)

    new_grid = copy.deepcopy(grid)
    for w,z,y,x in [ [w,z,y,x] for w in range(1, len(grid)-1) for z in range(1, len(grid[w])-1) for y in range(1, len(grid[w][z])-1) for x in range(1, len(grid[w][z][y])-1) ]:
        total_neighbors = sum(grid[w+dw][z+dz][y+dy][x+dx] for dw,dz,dy,dx in [ [dw,dz,dy,dx] for dw in range(-1, 2) for dz in range(-1, 2) for dy in range(-1, 2) for dx in range(-1, 2) if not(dw==dx==dy==dz==0)])
        if new_grid[w][z][y][x]:
            new_grid[w][z][y][x] = True if total_neighbors in [2,3] else False
        else:
            new_grid[w][z][y][x] = True if total_neighbors == 3 else False
    return(new_grid)

def puzzles(input_lines, **extra_args):
    grid = [ [ [] ] ]
    for line in input_lines:
        grid[0][0].append( [ i == '#' for i in line ] )

    extend_grid(grid)
    for _ in range(6):
        grid = next_grid(grid)

    yield(None)
    yield(sum(grid[w][z][y][x] for w,z,y,x in [ [w,z,y,x] for w in range(len(grid)) for z in range(len(grid[w])) for y in range(len(grid[w][z])) for x in range(len(grid[w][z][y])) ]))

aoc.run(puzzles)
