#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import itertools

def puzzles(input_lines, **extra_args):
    position_characters = None
    for line in input_lines:
        if position_characters is None:
            position_characters = [ "" ] * len(line)
        for i in range(len(line)):
            position_characters[i] += line[i]

    yield("".join(sorted([ len(list(g)), c ] for c,g in itertools.groupby(sorted(position_characters[i])))[-1][1] for i in range(len(position_characters))))
    yield("".join(sorted([ len(list(g)), c ] for c,g in itertools.groupby(sorted(position_characters[i])))[0][1] for i in range(len(position_characters))))

aoc.run(puzzles, samples = { 1: [ "easter", "advent" ] })
