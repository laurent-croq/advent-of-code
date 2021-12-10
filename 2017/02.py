#!/usr/bin/python3

import aoc

from itertools import combinations,filterfalse,permutations

def puzzles(input_lines, **extra_args):
    yield (
        sum(
            max(numbers)-min(numbers) for numbers in [ list(map(int, line.split())) for line in input_lines ]
        )
    )

    yield (
        sum(
            sum(
                sum(
                    n1//n2 for n1,n2 in filterfalse(lambda c: c[0] % c[1] > 0, permutations(couple))
                ) for couple in combinations(numbers,2)
            ) for numbers in [ list(map(int, line.split())) for line in input_lines ]
        )
    )

aoc.run(puzzles, samples = { 1: (18,32), 2: (18,9) })