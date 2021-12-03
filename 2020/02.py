#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import re

def puzzles(input_lines, **extra_args):
    answer1 = answer2 = 0
    for val1,val2,char,password in [ [ int(f[0]), int(f[1]), f[2], f[3] ] for f in [ re.sub(r"^(\d+)-(\d+) (\w): (\w*)", r"\1:\2:\3:\4", line).split(":") for line in input_lines ] ]:
        c = password.count(char)
        answer1 += c>=val1 and c<=val2
        answer2 += (password[val1-1] == char) != (password[val2-1] == char)

    yield(answer1)
    yield(answer2)

aoc.run(puzzles, samples = { 1: [ 2, 1 ] })
