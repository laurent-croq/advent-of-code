#!/usr/bin/python3

import aoc

def puzzles(input_lines, **extra_args):
    stream = input_lines[0]

    current_level = 0
    idx = 0
    answer_part1 = 0
    answer_part2 = 0
    while idx < len(stream):
        if stream[idx] == '{':
            current_level += 1
        elif stream[idx] == '}':
            answer_part1 += current_level
            current_level -= 1
        elif stream[idx] == '<':
            idx += 1
            while stream[idx] != '>':
                if stream[idx] == '!':
                    idx += 2
                else:
                    idx += 1
                    answer_part2 += 1

        idx += 1

    yield(answer_part1)
    yield(answer_part2)

aoc.run(puzzles)