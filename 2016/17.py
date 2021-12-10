#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

from heapq import heappop,heappush
from hashlib import md5

def find_shortest_path(passcode):
    paths = []
    heappush(paths, [ 0, "", (0,0) ])
    previous = []
    while True:
        if len(paths) == 0:
            return(None)
        length, path, pos = heappop(paths)
#        print("Handling %s at %s" % (path, pos))
        if pos == (3,3):
            return(path)
        if path in previous:
            continue
        previous.append(path)
        doors = md5((passcode+path).encode('utf-8')).hexdigest()[:4]
        if pos[0]>0 and doors[0] in "bcdef":
            heappush(paths, (length+1, path+"U", (pos[0]-1, pos[1])))
        if pos[0]<3 and doors[1] in "bcdef":
            heappush(paths, (length+1, path+"D", (pos[0]+1, pos[1])))
        if pos[1]>0 and doors[2] in "bcdef":
            heappush(paths, (length+1, path+"L", (pos[0], pos[1]-1)))
        if pos[1]<3 and doors[3] in "bcdef":
            heappush(paths, (length+1, path+"R", (pos[0], pos[1]+1)))

def find_longest_path(passcode):
    paths = []
    heappush(paths, [ 0, "", (0,0) ])
    previous = []
    longest = 0
    while True:
        if len(paths) == 0:
            break
        length, path, pos = heappop(paths)
#        print("Handling %s at %s" % (path, pos))
        if pos == (3,3):
            if length > longest:
                longest = length
            continue
        if path in previous:
            continue
        previous.append(path)
        doors = md5((passcode+path).encode('utf-8')).hexdigest()[:4]
        if pos[0]>0 and doors[0] in "bcdef":
            heappush(paths, (length+1, path+"U", (pos[0]-1, pos[1])))
        if pos[0]<3 and doors[1] in "bcdef":
            heappush(paths, (length+1, path+"D", (pos[0]+1, pos[1])))
        if pos[1]>0 and doors[2] in "bcdef":
            heappush(paths, (length+1, path+"L", (pos[0], pos[1]-1)))
        if pos[1]<3 and doors[3] in "bcdef":
            heappush(paths, (length+1, path+"R", (pos[0], pos[1]+1)))

    return(longest)
    
def puzzles(input_lines, **extra_args):
    passcode = input_lines[0]

    yield(find_shortest_path(passcode))

    yield(find_longest_path(passcode))

aoc.run(puzzles)
