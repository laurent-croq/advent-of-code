#!/usr/bin/python3

import aoc

def puzzles(input_lines):
    input_numbers = [ int(n) for n in input_lines ]
    answer1 = answer2 = None
    for i, n in enumerate(input_numbers):
        if 2020-n in input_numbers[i+1:]:
            answer1 = n*(2020-n)
            yield(answer1)
            if answer2 is not None:
                yield(answer2)

        for j, m in enumerate(input_numbers[i+1:]):
            if 2020-n-m in input_numbers[j+1:]:
                answer2 = n*m*(2020-n-m)
                if answer1 is not None:
                    yield(answer2)

aoc.run(puzzles)
