#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def solve_puzzle(input_lines, **extra_args):
    answer1 = 0
    answer2 = 0

    links = {}
    for src,dest in [ line.split("-") for line in input_lines ]:
        links[src] = links.get(src, []) + [ dest ]
        links[dest] = links.get(dest, []) + [ src ]

    stack = [ [False, ep] for ep in links["start"] ]

    while len(stack) > 0:
        path = stack.pop()
        for dest in links[path[-1]]:
            if dest == "start":
                continue
            elif dest == "end":
                answer1 += (path[0] == False)
                answer2 += 1
            elif dest.isupper() or dest not in path:
                stack.append(path+[dest])
            elif not path[0]:
                stack.append([True]+path[1:]+[dest])

    yield answer1
    yield answer2

aoc.run(solve_puzzle, samples = { 1: [10, 36], 2: [19, 103], 3: [226, 3509] } )
