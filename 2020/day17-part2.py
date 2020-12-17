#!/usr/bin/python3

import aoc
puzzle_lines = aoc.read_puzzle_input()

grid = [ [ [] ] ]

for line in puzzle_lines:
    grid[0][0].append( [ i == '#' for i in line ] )

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

def dump_grid(grid):
    for w, cube in enumerate(grid):
        for z, layer in enumerate(cube):
            print("z=%d, w=%d" % (z,w))
            for y, line in enumerate(layer):
                print("%s (y=%d)" % ("".join([ "#" if p else "." for p in line ]), y))
            print

def neighors(grid, x, y, z, w):
    total = 0
    for dw in range(-1, 2):
        for dz in range(-1, 2):
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx==dy==dz==dw==0:
                        continue
                    else:
                        total += grid[w+dw][z+dz][y+dy][x+dx]
    return(total)

def next_grid(grid):
    extend_grid(grid)

    new_grid = copy.deepcopy(grid)

    for w in range(1, len(grid)-1):
        for z in range(1, len(grid[w])-1):
            for y in range(1, len(grid[w][z])-1):
                for x in range(1, len(grid[w][z][y])-1):
                    total = neighors(grid, x, y, z, w)
                    if new_grid[w][z][y][x]:
                        new_grid[w][z][y][x] = True if total in [2,3] else False
                    else:
                        new_grid[w][z][y][x] = True if total == 3 else False
    return(new_grid)

def sum_grid(grid):
    total = 0
    for w in range(len(grid)):
        for z in range(len(grid[w])):
            for y in range(len(grid[w][z])):
                for x in range(len(grid[w][z][y])):
                    total += grid[w][z][y][x]
    return(total)

extend_grid(grid)
for _ in range(6):
    new_grid = next_grid(grid)
    grid = new_grid

print("answer2 = %d" % sum_grid(new_grid))
