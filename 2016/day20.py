#!/usr/bin/python3

import aoc

from itertools import filterfalse

def puzzles(input_lines, **extra_args):
    blocked_ranges = {}

    for begin,end in [ map(int, line.split("-")) for line in input_lines ]:
        overlaps = list(filterfalse(lambda b: b>end+1 or blocked_ranges[b]<begin-1, blocked_ranges))
        begin = min(overlaps+[begin])
        end = max([ blocked_ranges[o] for o in overlaps ]+[end])
        for o in overlaps:
            del blocked_ranges[o]
        blocked_ranges[begin] = end

    yield(blocked_ranges[0]+1)
    yield(4294967296 - sum(map(lambda b: blocked_ranges[b]-b+1, blocked_ranges)))

aoc.run(puzzles)