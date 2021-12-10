#!/usr/bin/python3

import aoc

def generator(value, factor, mask=None):
    while True:
        value = (value*factor)%2147483647
        if mask is None or value & mask == 0:
            yield(value)

def puzzles(input_lines, **extra_args):
    if not extra_args['skip1']:
        answer_part1=0
        genA = generator(int(input_lines[0].split()[-1]), 16807)
        genB = generator(int(input_lines[1].split()[-1]), 48271)

        for _ in range(40_000_000):
            valueA = next(genA)
            valueB = next(genB)
            if (valueA & 0xFFFF) == (valueB & 0xFFFF):
                answer_part1 += 1
            
        yield(answer_part1)
    else:
        yield(None)

    if not extra_args['skip2']:
        answer_part2 = 0
        genA = generator(int(input_lines[0].split()[-1]), 16807, mask=3)
        genB = generator(int(input_lines[1].split()[-1]), 48271, mask=7)

        for _ in range(5_000_000):
            valueA = next(genA)
            valueB = next(genB)
            if (valueA & 0xFFFF) == (valueB & 0xFFFF):
                answer_part2 += 1
            
        yield(answer_part2)
    else:
        yield(None)

aoc.run(puzzles)