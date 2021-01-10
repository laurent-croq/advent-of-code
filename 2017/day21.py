#!/usr/bin/python3.8

import aoc

import math
from copy import deepcopy

def all_patterns(ptn_source):
    for ptn in [ ptn_source, ptn_source[::-1] ]:
        yield(ptn)
        for _ in range(3):
            ptn = list("".join(l) for l in [ l for l in zip(*ptn[::-1]) ])
            yield(ptn)

def dump_pattern(msg, ptn):
    print("%s (%d):" % (msg, sum(p.count("#") for p in ptn)))
    print("\n".join(ptn))
    print("==> size = %d" % len(ptn))

def transform_pattern(transforms, ptn_source):

    divider = 3 if len(ptn_source)%3 == 0 else 2

    if len(ptn_source) == divider:
        return(transforms["".join(ptn_source)])

    final_pattern = []
    inner_size = len(ptn_source)//divider
    for y in range(divider):
        tmp_pattern = None
        for x in range(divider):
            new_pattern = transform_pattern(transforms, [ptn_source[y*inner_size+r][x*inner_size:(x+1)*inner_size] for r in range(inner_size) ])
            if tmp_pattern is None:
                tmp_pattern = deepcopy(new_pattern)
            else:
                tmp_pattern = [ "".join(l) for l in zip(tmp_pattern, new_pattern) ]
        final_pattern.extend(tmp_pattern)
    return(final_pattern)

def puzzles(input_lines, **extra_args):
    transforms = {}
    for ptn_source, ptn_dest in [ [ p[0].split("/"), p[1].split("/") ] for p in [ line.split(" => ") for line in input_lines ] ]:
        for ptn in all_patterns(ptn_source):
            transforms["".join(ptn)] = ptn_dest

    grid = [ ".#.", "..#", "###" ]
    for i in range(18):
        grid = transform_pattern(transforms, grid)
        if i == 4:
            yield(sum(p.count("#") for p in grid))

    yield(sum(p.count("#") for p in grid))

aoc.run(puzzles)