#!/usr/bin/python3

import aoc
puzzle_adapters = [ int(line) for line in aoc.read_puzzle_input() ]

def find_longest(adapts, jolts):
    if len(adapts) == 0:
        return([])
    diff = 1 if jolts+1 in adapts else 3
    return([diff] + find_longest(adapts[:adapts.index(jolts+diff)] + adapts[adapts.index(jolts+diff)+1:], jolts+diff))

longest = find_longest(puzzle_adapters, 0)

print("answer1 = %d" % (longest.count(1) * (longest.count(3)+1)))

from itertools import groupby

answer2 = 1
for diff, nb_adapts in [ [ d, len(list(l)) ] for d, l in groupby(longest) if d<3 ]:
    answer2 *= [ None, 1, 2, 4, 7, 13 ][nb_adapts] if diff==1 else (1 if nb_adapts == 1 else 2*(nb_adapts-1))

print("answer2 = %d" % answer2)
