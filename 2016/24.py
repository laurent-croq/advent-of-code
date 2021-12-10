#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

from itertools import combinations
from heapq import heappop,heappush

def find_next_hop(maze, previous_pos, pos, distance, target_pos):
    while pos != target_pos:
        ways = [ (dy,dx) for dx in range(-1,2) for dy in range(-1,2) if abs(dx)+abs(dy)==1 and maze[pos[0]+dy][pos[1]+dx] != '#' and (pos[0]+dy,pos[1]+dx) != previous_pos ]
        if len(ways)!=1:
            return(distance, pos)
        (previous_pos, pos) = (pos, tuple(map(sum, zip(pos, ways[0]))))
        distance += 1
    return(distance, pos)

def get_distance(maze, pos1, pos2):
    states = []
    heappush(states, (0, pos1))
    best_distance = None
    previous = []
    while len(states)>0:
        distance, pos = heappop(states)
        if pos == pos2:
            if best_distance is None or distance < best_distance:
                best_distance = distance
            continue
        if pos in previous:
            # Consider best distance to this point?
            continue
        previous.append(pos)
        for dx,dy in [ (dx,dy) for dx in range(-1,2) for dy in range(-1,2) if abs(dx)+abs(dy)==1 and maze[pos[0]+dy][pos[1]+dx] != '#' ]:
            heappush(states, find_next_hop(maze, pos, (pos[0]+dy, pos[1]+dx), distance+1, pos2))
    return(best_distance)

def puzzles(input_lines, **extra_args):
    maze = [ list(line) for line in input_lines ]
    width = len(maze[0])
    height = len(maze)
    
    changed = True
    while changed:
        changed = False
        for x,y in [ (x,y) for x in range(1,width-1) for y in range(1, height-1) ]:
            if maze[y][x] == "." and ((maze[y-1][x]=="#") + (maze[y+1][x]=="#") + (maze[y][x-1]=="#") + (maze[y][x+1]=="#")) >= 3:
                maze[y][x] = "#"
                changed = True

    numbers = {}
    for y in range(len(maze)):
        for c in "".join(maze[y]).replace("#", "").replace(".", ""):
            numbers[c] = (y, maze[y].index(c))

    distances = dict( [ n1, dict([n2, None] for n2 in numbers if n1!=n2) ] for n1 in numbers )
    for n1,n2 in combinations(numbers, 2):
        distances[n1][n2] = distances[n2][n1] = get_distance(maze, numbers[n1], numbers[n2])

    states = []
    heappush(states, (0, ['0']))
    answer_part1 = None
    answer_part2 = None
    while len(states)>0:
        distance, explored = heappop(states)
        if len(explored) == len(numbers):
            if answer_part1 is None:
                answer_part1 = distance
            if answer_part2 is None:
                answer_part2 = distance+distances[explored[-1]]['0']
            else:
                answer_part2 = min(answer_part2, distance+distances[explored[-1]]['0'])
            continue

        for n in set(numbers).difference(explored):
            heappush(states, (distance+distances[explored[-1]][n], explored+[n]))

    yield(answer_part1)
    yield(answer_part2)

aoc.run(puzzles)
