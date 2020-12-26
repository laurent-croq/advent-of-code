#!/usr/bin/python3

import aoc
puzzle_lines = aoc.load_puzzle_input()

import re,copy
def identify_tile(coord, moves):
    while moves != "":
        m = re.match('^(w|e|sw|se|nw|ne)(.*)', moves)
        move = m.group(1)
        moves = m.group(2)
        if len(move) == 1:
            coord[1] += (move=="e")*2-1
        else:
            coord[0] += coord[2] + (move[0]=="n") - 1
            coord[1] += coord[2] + (move[1]=="e") - 1
            coord[2] = not(coord[2])
        
def extend_grid(grid, coord, center=None):
    empty_cell = [ False, False ]
    width,height = len(grid[0]),len(grid)
    if coord[0] >= height:
        for _ in range(coord[0]-height+1):
            grid.append( [ empty_cell[:] for _ in range(width) ] )
    elif coord[0] < 0:
        for _ in range(-coord[0]):
            grid.insert(0, [ empty_cell[:] for _ in range(width) ] )
        if center is not None:
            center[0] -= coord[0]
        coord[0] = 0

    if coord[1] >= width:
        for l in grid:
            l.extend([ empty_cell[:] for _ in range(coord[1]-width+1) ])
    elif coord[1] < 0:
        for l in grid:
            l[0:0] = [ empty_cell[:] for _ in range(-coord[1]) ]
        if center is not None:
            center[1] -= coord[1]
        coord[1] = 0

def total_black_tiles(grid):
    return(sum(grid[y][x][b] for y,x,b in [ [y,x,b] for y in range(len(grid)) for x in range(len(grid[0])) for b in range(2) ]))

def get_adjacent_coords(coord):
    delta = coord[2]*2-1
    return([
        [ coord[0], coord[1], 1-coord[2] ],
        [ coord[0], coord[1]+delta, coord[2] ],
        [ coord[0], coord[1]+delta, 1-coord[2] ],
        [ coord[0], coord[1]-delta, coord[2] ],
        [ coord[0]+delta, coord[1], 1-coord[2] ],
        [ coord[0]+delta, coord[1]+delta, 1-coord[2] ]
    ])

def total_black_adjacents(grid, coord):
    return(sum(grid[c[0]][c[1]][c[2]] for c in [ c for c in get_adjacent_coords(coord) if c[0] in range(0,len(grid)) and c[1] in range(0,len(grid[0])) ]))

def next_grid(grid):
    new_grid = copy.deepcopy(grid)

    for y,x,b in [ [y,x,b] for y in range(len(grid)) for x in range(len(grid[0])) for b in range(2) ]:
        new_grid[y][x][b] = (total_black_adjacents(grid, [y,x,b]) in [1,2]) if grid[y][x][b] else (total_black_adjacents(grid, [y,x,b])==2)

    return(new_grid)

center = [ 0, 0, 0 ]
grid = [ [ [ False, False ] ] ]

for line in puzzle_lines:
    coord = center[:]
    identify_tile(coord, line)
    extend_grid(grid, coord, center)

    grid[coord[0]][coord[1]][coord[2]] = not(grid[coord[0]][coord[1]][coord[2]])

print("answer1 = %d" % total_black_tiles(grid))

for day in range(100):
    if sum([ sum(grid[0][x][b] for b in range(2)) for x in range(len(grid[0])) ]) > 0:
        extend_grid(grid, [-1,0])
    if sum([ sum(grid[y][0][b] for b in range(2)) for y in range(len(grid)) ]) > 0:
        extend_grid(grid, [0,-1])
    if sum([ sum(grid[len(grid)-1][x][b] for b in range(2)) for x in range(len(grid[0])) ]) > 0:
        extend_grid(grid, [len(grid),0])
    if sum([ sum(grid[y][len(grid[0])-1][b] for b in range(2)) for y in range(len(grid)) ]) > 0:
        extend_grid(grid, [0,len(grid[0])])
    grid = next_grid(grid)

print("answer2 = %d" % total_black_tiles(grid))