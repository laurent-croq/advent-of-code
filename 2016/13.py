#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import heapq

def is_empty(x, y, favorite_number):
    return(bin(x*x+3*x+2*x*y+y+y*y+favorite_number).count("1") % 2 == 0)

def distance(pos1, pos2):
    return(abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1]))

def find_path(start_pos, end_pos, favorite_number, max_distance=None):
    positions = []
    distances = {}

    heapq.heappush(positions, (0, distance(start_pos, end_pos), start_pos))

    while len(positions)>0:
        distance_to_start, distance_to_end, pos = heapq.heappop(positions)
        if distance_to_end==0:
            return(distance_to_start, len(distances))

        if max_distance is not None and distance_to_start==max_distance:
            continue        
        for dx,dy in [ [dx,dy] for dx,dy in [ [-1,0], [1,0], [0,-1], [0,1] ] if pos[0]+dx>=0 and pos[1]+dy>=0 and is_empty(pos[0]+dx, pos[1]+dy, favorite_number) ]:
            new_pos = (pos[0]+dx, pos[1]+dy)
            if new_pos in distances:
                if distance_to_start+1 < distances[new_pos]:
                    distances[new_pos] = distance_to_start+1
            else:
                heapq.heappush(positions, [ distance_to_start+1, distance(new_pos, end_pos), new_pos ])
                distances[new_pos] = distance_to_start+1

    return(None, len(distances))

def puzzles(input_lines, **extra_args):
    favorite_number = int(input_lines[0])

    yield(find_path([1,1], [31,39], favorite_number)[0])
    yield(find_path([1,1], [31,39], favorite_number, max_distance=50)[1])

aoc.run(puzzles)
