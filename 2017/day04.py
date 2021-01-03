#!/usr/bin/python3

import aoc

from itertools import combinations

def puzzles(input_lines, **extra_args):
    answer_part1 = 0
    answer_part2 = 0
    for passphrase in input_lines:
        for w1,w2 in combinations(passphrase.split(),2):
            if w1 == w2:
                break
        else:
            answer_part1 += 1

    yield(answer_part1)

    for passphrase in input_lines:
        for w1,w2 in combinations(passphrase.split(),2):
            if sorted(list(w1)) == sorted(list(w2)):
                break
        else:
            answer_part2 += 1

    yield(answer_part2)

aoc.run(puzzles)