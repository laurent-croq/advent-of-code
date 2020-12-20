#!/usr/bin/python3

import os, sys
sys.path.insert(1, os.getcwd()+"/..")
import aoc
puzzle_lines = aoc.load_puzzle_input()

import re
import math
import itertools

def get_borders(bitmap):
    borders = []
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", bitmap[0])), 2))
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", "".join(l[-1] for l in bitmap))), 2))
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", bitmap[-1])), 2))
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", "".join(l[0] for l in bitmap))), 2))
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", bitmap[0][::-1])), 2))
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", "".join(l[0] for l in bitmap[::-1]))), 2))
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", bitmap[-1][::-1])), 2))
    borders.append(int("0b"+re.sub("#", "1", re.sub(r'\.', "0", "".join(l[-1] for l in bitmap[::-1]))), 2))
    return(borders)

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

corners = [ t for t in tiles if len(tiles[t]['neighbors']) == 2 ]
print("answer1 = %d" % math.prod(corners))

max_tiles = int(math.sqrt(len(tiles)))
grid = [ [ None for _ in range(max_tiles) ] for _ in range(max_tiles) ]
remaining_tiles = list(tiles)

def position_tile(t, n, flip_h=False, flip_v=False):
    for _ in range(n):
        tiles[t]['bitmap'] = list("".join(l) for l in [ l for l in zip(*tiles[t]['bitmap'][::-1]) ] )
    
    if flip_v:
        for b in range(len(tiles[t]['bitmap'])):
            tiles[t]['bitmap'][b] = tiles[t]['bitmap'][b][::-1]

    if flip_h:
        tiles[t]['bitmap'] = tiles[t]['bitmap'][::-1]

    tiles[t]['borders'] = get_borders(tiles[t]['bitmap'])

for y in range(max_tiles):
    for x in range(max_tiles):
        if y == 0:
            if x == 0:
                tile = corners[0]
            else:
                tile = [ t for t in remaining_tiles if tiles[grid[0][x-1]]['borders'][1] in tiles[t]['borders'] ][0]
                
                position_tile
                idx = tiles[tile]['borders'].index(tiles[grid[0][x-1]]['borders'][1])
                position_tile(tile, (7-idx)%4) #, flip_v=(idx>=4))

                idx = tiles[tile]['borders'].index(tiles[grid[0][x-1]]['borders'][1])
                if idx>=4:
                    position_tile(tile, 0, flip_h=True)
                    idx = tiles[tile]['borders'].index(tiles[grid[0][x-1]]['borders'][1])
                if idx%4 == 1:
                    position_tile(tile, 0, flip_v=True)
                    idx = tiles[tile]['borders'].index(tiles[grid[0][x-1]]['borders'][1])
        else:
            tile = [ t for t in remaining_tiles if tiles[grid[y-1][x]]['borders'][2] in tiles[t]['borders'] ][0]

            idx = tiles[tile]['borders'].index(tiles[grid[y-1][x]]['borders'][2])
            position_tile(tile, (6-idx)%4) #, flip_h=(idx>=4))

            idx = tiles[tile]['borders'].index(tiles[grid[y-1][x]]['borders'][2])
            position_tile(tile, 0, flip_h=(idx%4 == 2), flip_v=(idx>=4))

        grid[y][x] = tile
        remaining_tiles.remove(tile)

bitmap = [ "" for _ in range(8*max_tiles) ]

for y in range(max_tiles):
    for x in range(max_tiles):
        for b in range(8):
            bitmap[y*8+b] += tiles[grid[y][x]]['bitmap'][b+1][1:-1]

def find_monster(bitmap):
    monster = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   "
        ]
    offsets = []

    for x,y in [ [x,y] for y in range(len(monster)) for x in range(len(monster[y])) if monster[y][x] == "#" ]:
        offsets.append( [ y, x ] )
    
    found = 0
    for x,y in [ [x,y] for y in range(0,len(bitmap)-len(monster)+1) for x in range(0, len(bitmap[y])-len(monster[0])+1) ]:
        for o in offsets:
            if bitmap[y+o[0]][x+o[1]] != "#":
                break
        else:
            found += 1

    return(None if found==0 else sum([ line.count('#') for line in bitmap ])-found*len(offsets))

for i in range(8):
    answer2 = find_monster(bitmap)
    if answer2 is not None:
        print("answer2 = %d" % answer2)
        break

    bitmap = list("".join(l) for l in [ l for l in zip(*bitmap[::-1]) ] )

    if i == 4:
        bitmap = bitmap[::-1]
