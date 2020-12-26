#!/usr/bin/python3

import aoc
puzzle_lines = aoc.load_puzzle_input()

import re, math, itertools

def get_borders(bitmap):
    borders = []

    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", bitmap[0])), 2))
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", "".join(l[-1] for l in bitmap))), 2))
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", bitmap[-1])), 2))
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", "".join(l[0] for l in bitmap))), 2))

    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", bitmap[0][::-1])), 2))
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", "".join(l[-1] for l in bitmap[::-1]))), 2))
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", bitmap[-1][::-1])), 2))
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", "".join(l[0] for l in bitmap[::-1]))), 2))

    return(borders)

def position_corner(tile):
    idx = min([ tiles[tile]['borders'].index(b) for b in set(tiles[tile]['borders']).intersection(set(tiles[tiles[tile]['neighbors'][0]]['borders']).union(tiles[tiles[tile]['neighbors'][1]]['borders']))])
    for _ in range((5-idx)%4):
        tiles[tile]['bitmap'] = list("".join(l) for l in [ l for l in zip(*tiles[tile]['bitmap'][::-1]) ])
    tiles[tile]['borders'] = get_borders(tiles[tile]['bitmap'])

def position_tile(tile, link_tile, direction):
    for _ in range((6+direction-tiles[tile]['borders'].index(tiles[link_tile]['borders'][direction]))%4):
        tiles[tile]['bitmap'] = list("".join(l) for l in [ l for l in zip(*tiles[tile]['bitmap'][::-1]) ])  # Rotation
    
    tiles[tile]['borders'] = get_borders(tiles[tile]['bitmap'])
    if tiles[tile]['borders'].index(tiles[link_tile]['borders'][direction]) >= 4:
        if direction == 1:
            tiles[tile]['bitmap'] = tiles[tile]['bitmap'][::-1] # Vertical flip
        else:
            tiles[tile]['bitmap'] = [ tiles[tile]['bitmap'][b][::-1] for b in range(len(tiles[tile]['bitmap'])) ]   # Horizontal flip
        tiles[tile]['borders'] = get_borders(tiles[tile]['bitmap'])

def find_monster(bitmap):
    monster = [ "                  # ",
                "#    ##    ##    ###",
                " #  #  #  #  #  #   " ]
    offsets = []

    for y,x in [ [y,x] for y in range(len(monster)) for x in range(len(monster[y])) if monster[y][x] == "#" ]:
        offsets.append( [ y, x ] )
    
    found = 0
    for y,x in [ [y,x] for y in range(0,len(bitmap)-len(monster)+1) for x in range(0, len(bitmap[y])-len(monster[0])+1) ]:
        for o in offsets:
            if bitmap[y+o[0]][x+o[1]] != "#":
                break
        else:
            found += 1

    return(None if found==0 else sum([ line.count('#') for line in bitmap ])-found*len(offsets))

tiles = {}
bitmap = []
tile_num = None
for line in puzzle_lines:
    if line == "":
        tiles[tile_num] = { "bitmap": bitmap, "borders": get_borders(bitmap), "neighbors": [] }
        bitmap = []
        tile_num = None
    elif tile_num is None:
        tile_num = int(line[5:-1])
    else:
        bitmap.append(line)
    
for t1, t2 in itertools.combinations(tiles, 2):
    if len(set(tiles[t1]['borders']).intersection(set(tiles[t2]['borders']))) >= 2:
        tiles[t1]['neighbors'].append(t2)
        tiles[t2]['neighbors'].append(t1)

corner_tiles = [ t for t in tiles if len(tiles[t]['neighbors']) == 2 ]
print("answer1 = %d" % math.prod(corner_tiles))

puzzle_size = int(math.sqrt(len(tiles)))
puzzle = [ [ None for _ in range(puzzle_size) ] for _ in range(puzzle_size) ]

remaining_tiles = list(tiles)

for y,x in [ [y,x] for y in range(puzzle_size) for x in range(puzzle_size) ]:
    if y == 0:
        if x == 0:
            tile = corner_tiles[2]
            position_corner(tile)
        else:
            tile = [ t for t in remaining_tiles if tiles[puzzle[0][x-1]]['borders'][1] in tiles[t]['borders'] ][0]
            position_tile(tile, puzzle[0][x-1], 1)
    else:
        tile = [ t for t in remaining_tiles if tiles[puzzle[y-1][x]]['borders'][2] in tiles[t]['borders'] ][0]
        position_tile(tile, puzzle[y-1][x], 2)

    puzzle[y][x] = tile
    remaining_tiles.remove(tile)

bitmap = [ "" for _ in range(8*puzzle_size) ]
for y,x,b in [ [y,x,b] for y in range(puzzle_size) for x in range(puzzle_size) for b in range(8) ]:
    bitmap[y*8+b] += tiles[puzzle[y][x]]['bitmap'][b+1][1:-1]

for i in range(12):
    answer2 = find_monster(bitmap)
    if answer2 is not None:
        print("answer2 = %d" % answer2)
        break

    bitmap = list("".join(l) for l in [ l for l in zip(*bitmap[::-1]) ])    # Rotation
    if i == 4:
        bitmap = bitmap[::-1]   # Vertical flip
    elif i == 8:
        bitmap = [ bitmap[b][::-1] for b in range(len(bitmap)) ]    # Horizontal flip
