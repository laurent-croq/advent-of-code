#!/usr/bin/python3

import aoc

import math

def idx2coord(idx, center=(0,0)):
    if idx == 1:
        return(center)
        
    square_dim = 1+2*( int(math.sqrt(idx-1)+1)//2 )
    square_pos = idx-(square_dim-2)**2-1

    for side in [ side for side in range(4) if side*(square_dim-1) <= square_pos < (side+1)*(square_dim-1) ]:
        pos = [ (square_dim//2) * (-1 if side>1 else 1), (square_pos - square_dim//2 - side*(square_dim-1) + 1) * (-1 if 3>side>0 else 1) ][::1 if side%2==0 else -1]

    return(pos[0]+center[0], pos[1]+center[1])

def puzzles(input_lines, **extra_args):
    data_idx = int(input_lines[0])

    pos = idx2coord(data_idx)
    yield(abs(pos[1])+abs(pos[0]))

    grid_dim = 1+2*( int(math.sqrt(data_idx-1)+1)//2 )
    grid = [ [0] * grid_dim for _ in range(grid_dim) ]
    center = [ grid_dim//2, grid_dim//2 ]

    grid[center[1]][center[0]] = 1
    for idx in range(1, data_idx):
        pos = idx2coord(idx, center)
        grid[pos[1]][pos[0]] = sum(grid[pos[1]+dy][pos[0]+dx] for dx in range(-1,2) for dy in range(-1,2))
        if grid[pos[1]][pos[0]] > data_idx:
            break
    yield(grid[pos[1]][pos[0]])

aoc.run(puzzles)
