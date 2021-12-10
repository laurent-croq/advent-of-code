#!/usr/bin/python3

import aoc

def puzzles(input_lines, **extra_args):
    offsets_part1 = [ int(n) for n in input_lines ]
    offsets_part2 = offsets_part1[:]

    idx = 0
    answer_part1 = 0
    while 0 <= idx < len(offsets_part1):
        answer_part1 += 1
        next_idx = idx+offsets_part1[idx]
        offsets_part1[idx] = offsets_part1[idx]+1
        idx = next_idx
    yield(answer_part1)

    idx = 0
    answer_part2 = 0
    while 0 <= idx < len(offsets_part2):
        answer_part2 += 1
        next_idx = idx+offsets_part2[idx]
        offsets_part2[idx] = offsets_part2[idx] + (1 if offsets_part2[idx] <3 else -1)
        idx = next_idx
    yield(answer_part2)

aoc.run(puzzles)