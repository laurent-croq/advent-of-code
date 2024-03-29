#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def do_moves(initial_cups, max_cups=None, total_rounds=100):
    ring = {}
    for i,c in enumerate(initial_cups[:-1]):
        ring[int(c)] = int(initial_cups[i+1])

    if max_cups is None:
        ring[int(initial_cups[-1])] = int(initial_cups[0])
    else:
        ring[int(initial_cups[-1])] = len(initial_cups)+1
        for i in range(len(initial_cups)+1,max_cups):
            ring[i] = i+1

        ring[max_cups] = int(initial_cups[0])

    current = int(initial_cups[0])
    for _ in range(total_rounds):
        pickup = ring[current]
        ring[current] = ring[ring[ring[pickup]]]
        
        destination = 1+(current+len(ring)-2)%len(ring)
        while destination in [ pickup, ring[pickup], ring[ring[pickup]] ]:
            destination = 1+(destination+len(ring)-2)%len(ring)

        ring[ring[ring[pickup]]] = ring[destination]
        ring[destination] = pickup

        current = ring[current]

    if max_cups is None:
        res = ""
        current = 1
        for _ in range(len(initial_cups)-1):
            current = ring[current]
            res += str(current)

        return(res)
    else:
        return(ring[1] * ring[ring[1]])

def puzzles(input_lines, **extra_args):
    cups = [ int(c) for c in input_lines[0] ]
    yield(do_moves(cups))
    yield(do_moves(cups, max_cups=1_000_000, total_rounds=10_000_000))

aoc.run(puzzles)
