#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

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
        return(sum([ neighbors(grid[v[0]+delta], v[1:], sumnz+(delta!=0)) for delta in range(-1,2) ]))

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

def extend_grid_part1(grid):
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

def next_grid_part1(grid):
    extend_grid(grid)

    new_grid = copy.deepcopy(grid)
    for z,y,x in [ [z,y,x] for z in range(1, len(grid)-1) for y in range(1, len(grid[z])-1) for x in range(1, len(grid[z][y])-1) ]:
        total_neighbors = sum(grid[z+dz][y+dy][x+dx] for dz,dy,dx in [ [dz,dy,dx] for dz in range(-1, 2) for dy in range(-1, 2) for dx in range(-1, 2) if not(dx==dy==dz==0)])
        if new_grid[z][y][x]:
            new_grid[z][y][x] = True if total_neighbors in [2,3] else False
        else:
            new_grid[z][y][x] = True if total_neighbors == 3 else False
    return(new_grid)

def puzzles_part1(input_lines):
    grid = [ [] ]
    for line in input_lines:
        grid[0].append([ i == '#' for i in line ])

    extend_grid(grid)
    for _ in range(6):
        grid = next_grid_part1(grid)

    yield(sum(grid[z][y][x] for z,y,x in [ [z,y,x] for z in range(len(grid)) for y in range(len(grid[z])) for x in range(len(grid[z][y])) ]))

def extend_grid_part2(grid):
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

def next_grid_part2(grid):
    extend_grid(grid)

    new_grid = copy.deepcopy(grid)
    for w,z,y,x in [ [w,z,y,x] for w in range(1, len(grid)-1) for z in range(1, len(grid[w])-1) for y in range(1, len(grid[w][z])-1) for x in range(1, len(grid[w][z][y])-1) ]:
        total_neighbors = sum(grid[w+dw][z+dz][y+dy][x+dx] for dw,dz,dy,dx in [ [dw,dz,dy,dx] for dw in range(-1, 2) for dz in range(-1, 2) for dy in range(-1, 2) for dx in range(-1, 2) if not(dw==dx==dy==dz==0)])
        if new_grid[w][z][y][x]:
            new_grid[w][z][y][x] = True if total_neighbors in [2,3] else False
        else:
            new_grid[w][z][y][x] = True if total_neighbors == 3 else False
    return(new_grid)

def puzzles_part2(input_lines):
    grid = [ [ [] ] ]
    for line in input_lines:
        grid[0][0].append( [ i == '#' for i in line ] )

    extend_grid(grid)
    for _ in range(6):
        grid = next_grid_part2(grid)

    yield(sum(grid[w][z][y][x] for w,z,y,x in [ [w,z,y,x] for w in range(len(grid)) for z in range(len(grid[w])) for y in range(len(grid[w][z])) for x in range(len(grid[w][z][y])) ]))

def puzzles(input_lines, **extra_args):
    grid = []
    for line in input_lines:
        grid.append( [ i == '#' for i in line ] )

    yield(answer(grid[:], 3))
    yield(answer(grid[:], 4))

aoc.run(puzzles)
