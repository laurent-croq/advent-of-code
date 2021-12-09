#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def bassin_size(hm, hmtag, y0, x0, way=None):
    if hm[y0][x0] == 9 or hmtag[y0][x0]:
        return(0)

    print("Exploring at %d,%d" % (y0, x0))
    total = 0

    for x in range(x0, len(hm[y0])-1):
        if hm[y0][x] == 9:
            break
        total+=1
        hmtag[y0][x] = True
        if way == None or way == True:
            total += bassin_size(hm, hmtag, y0-1, x, True)
        if way == None or way == False:
            total += bassin_size(hm, hmtag, y0+1, x, False)

    for x in range(x0-1, 0, -1):
        if hm[y0][x] == 9:
            break
        total+=1
        hmtag[y0][x] = True
        if way == None or way == True:
            total += bassin_size(hm, hmtag, y0-1, x, True)
        if way == None or way == False:
            total += bassin_size(hm, hmtag, y0+1, x, False)

    return(total)

def solve_puzzle(input_lines, **extra_args):
    answer1 = 0
    answer2 = None

    hm = []
    for line in input_lines:
        hm.append( [ 9 ] + [ int(n) for n in line ] + [ 9 ] )
    
    hm.insert( 0, [9] * (len(hm[0])+2) )
    hm.append( [9] * (len(hm[0])+2) )

    hmtag = [ [False]*len(hm[0]) for _ in range(len(hm)) ]
    bassins = []

    for y in range(1,len(hm)-1):
        for x in range(1, len(hm[y])-1):
            if hm[y][x] < min(hm[y-1][x], hm[y+1][x], hm[y][x-1], hm[y][x+1]):
                answer1 += hm[y][x]+1
                #print("Found at %d,%d" % (y, x))
                #print(bassin_size(hm, hmtag, y, x))
                bassins.append(bassin_size(hm, hmtag, y, x))

    final = sorted(bassins)[-3:]

    yield answer1
    yield final[0]*final[1]*final[2]

aoc.run(solve_puzzle, samples = { 1: [15, 1134]} )
