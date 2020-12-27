#!/usr/bin/python3

import aoc

import itertools

def find_longest(adapters, jolts=0):
    if jolts == max(adapters)+3:
        return([])
    diff = 1 if jolts+1 in adapters else 3
    return([diff] + find_longest(adapters, jolts+diff))

def puzzles(input_lines):
    adapters = [ int(line) for line in input_lines ]
    longest = find_longest(adapters)

    yield(longest.count(1) * longest.count(3))

    answer2 = 1
    for diff, nb_adapters in [ [ d, len(list(l)) ] for d, l in itertools.groupby(longest) if d<3 ]:
        answer2 *= [ None, 1, 2, 4, 7, 13 ][nb_adapters] if diff==1 else (1 if nb_adapters == 1 else 2*(nb_adapters-1))

    yield(answer2)

aoc.run(puzzles)
