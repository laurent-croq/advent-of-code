#!/usr/bin/python3

import aoc

import re
from itertools import groupby

def sum_tower(programs, p):
    return(programs[p]["weight"] + sum( sum_tower(programs, p2) for p2 in programs[p]["subprogs"]))

def get_answer_part2(programs, prog, good_weight=None):
    if len(programs[prog]['subprogs']) == 0:
        return(good_weight)

    weights = sorted([ [ len(list(l)), w ] for w, l in groupby(sorted( sum_tower(programs, p) for p in programs[prog]['subprogs'] )) ])
    if len(weights) == 1:
        return(good_weight)

    unbalanced_tower = [ p for p in programs[prog]['subprogs'] if sum_tower(programs, p) == weights[0][1] ][0]
    return(get_answer_part2(programs, unbalanced_tower, programs[unbalanced_tower]['weight'] - weights[0][1] + weights[1][1]))

def puzzles(input_lines, **extra_args):
    programs = {}
    parents = {}

    for line in input_lines:
        m = re.match(r'(.*) \((\d+)\)( -> (.*))?', line)
        programs[m.group(1)] = { "weight": int(m.group(2)), "subprogs": m.group(4).split(", ") if m.group(3) is not None else [] }
        for subprog in programs[m.group(1)]['subprogs']:
            parents[subprog] = m.group(1)

    lowest = list(parents)[0]
    try:
        while True:
            lowest = parents[lowest]
    except:
        yield(lowest)

    yield(get_answer_part2(programs, lowest))

aoc.run(puzzles)