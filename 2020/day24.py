#!/usr/bin/python3

import aoc
puzzle_lines = aoc.load_puzzle_input()

import re
def identify_tile(coord, moves):
    while moves != "":
        m = re.match('^(w|e|sw|se|nw|ne)(.*)', moves)
        move = m.group(1)
        moves = m.group(2)
        if move == "w":
            coord[1] -= 1
        elif move == "e":
            coord[1] += 1
        elif move == "nw":
            coord[0] += 1 if coord[2] else 0
            coord[1] += 0 if coord[2] else -1
            coord[2] = not(coord[2])
        elif move == "ne":
            coord[0] += 1 if coord[2] else 0
            coord[1] += 1 if coord[2] else 0
            coord[2] = not(coord[2])
        elif move == "sw":
            coord[0] += 0 if coord[2] else -1
            coord[1] += 0 if coord[2] else -1
            coord[2] = not(coord[2])
        elif move == "se":
            coord[0] += 0 if coord[2] else -1
            coord[1] += 1 if coord[2] else 0
            coord[2] = not(coord[2])
        
        #print("%s ==> %s" % (move, coord))

def extend_grid(grid, coord, center=None):
    empty_cell = { False: False, True: False }
    width = len(grid[0])
    if coord[0] >= len(grid):
        for _ in range(coord[0]-len(grid)+1):
            grid.append( [ empty_cell.copy() for _ in range(width) ] )
    elif coord[0] < 0:
        for _ in range(-coord[0]):
            grid.insert(0, [ empty_cell.copy() for _ in range(width) ] )
        if center is not None:
            center[0] -= coord[0]
        coord[0] = 0

    if coord[1] >= width:
        for l in grid:
            l.extend([ empty_cell.copy() for _ in range(coord[1]-width+1) ])
    elif coord[1] < 0:
        for l in grid:
            l[0:0] = [ empty_cell.copy() for _ in range(-coord[1]) ]
        if center is not None:
            center[1] -= coord[1]
        coord[1] = 0

def total_black_tiles(grid):
    return(sum(grid[y][x][b] for y,x,b in [ [y,x,b] for y in range(len(grid)) for x in range(len(grid[0])) for b in [False, True] ]))

def get_adjacent_coords(coord):
    delta = 1 if coord[2] else -1
    return([
        [ coord[0], coord[1], not(coord[2]) ],
        [ coord[0], coord[1]+delta, coord[2] ],
        [ coord[0], coord[1]+delta, not(coord[2]) ],
        [ coord[0], coord[1]-delta, coord[2] ],
        [ coord[0]+delta, coord[1], not(coord[2]) ],
        [ coord[0]+delta, coord[1]+delta, not(coord[2]) ]
    ])

def total_black_adjacents(grid, coord):
#    total = 0
#    for coord in [ coord for coord in get_adjacent_coords(coord) if coord[0] in range(0,len(grid)) and coord[1] in range(0,len(grid[0])) ]:
#        total += grid[coord[0]][coord[1]][coord[2]]
#    return(total)
    return(sum(grid[coord[0]][coord[1]][coord[2]] for coord in [ coord for coord in get_adjacent_coords(coord) if coord[0] in range(0,len(grid)) and coord[1] in range(0,len(grid[0])) ]))

import copy
def next_grid(grid):
    new_grid = copy.deepcopy(grid)

    for y,x,b in [ [y,x,b] for y in range(len(grid)) for x in range(len(grid[0])) for b in [ False, True ] ]:
        total = total_black_adjacents(grid, [y,x,b])

        if grid[y][x][b]:
            new_grid[y][x][b] = (total in [1,2])
        else:
            new_grid[y][x][b] = (total==2)

    return(new_grid)

center = [ 0, 0, False ]
grid = [ [ { False: False, True: False } ] ]

for line in puzzle_lines:
    coord = center[:]
    identify_tile(coord, line)
    extend_grid(grid, coord, center)

    grid[coord[0]][coord[1]][coord[2]] = not(grid[coord[0]][coord[1]][coord[2]])

print("answer1 = %d" % total_black_tiles(grid))

def dump_grid(grid):
    for l in grid[::-1]:
        print("%s" % " ".join([ ("#" if t[False] else ".")+"\\"+("#" if t[True] else ".") for t in l ]))

for day in range(100):
    if sum([ sum(grid[0][x].values()) for x in range(len(grid[0])) ]) > 0:
        extend_grid(grid, [-1,0])
    if sum([ sum(grid[len(grid)-1][x].values()) for x in range(len(grid[0])) ]) > 0:
        extend_grid(grid, [len(grid),0])
    if sum([ sum(grid[y][0].values()) for y in range(len(grid)) ]) > 0:
        extend_grid(grid, [0,-1])
    if sum([ sum(grid[y][len(grid[0])-1].values()) for y in range(len(grid)) ]) > 0:
        extend_grid(grid, [0,len(grid[0])])
    grid = next_grid(grid)

print("answer2 = %d" % total_black_tiles(grid))