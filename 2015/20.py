#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def puzzles(input_lines, **extra_args):
    min_presents = int(input_lines[0])
    
    houses_part1 = [0] * (min_presents//10)
    houses_part2 = [0] * (min_presents//10)

    for i in range(1, min_presents//10):
        for j in range(i, min_presents//10, i):
            houses_part1[j]+=10*i
            if j <= i*50:
                houses_part2[j]+=11*i

    yield([ i for i in range(min_presents//10) if houses_part1[i]>=min_presents][0])
    yield([ i for i in range(min_presents//10) if houses_part2[i]>=min_presents][0])

aoc.run(puzzles)
