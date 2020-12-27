#!/usr/bin/python3

import aoc

def puzzles(input_lines):
    total_part1 = 0
    total_part2 = 0

    group_answers = {}
    group_size = 0
    for line in input_lines:
        if line == "":
            total_part1 += len(group_answers)
            total_part2 += sum(map(lambda a: group_answers[a] == group_size, group_answers))
            group_answers = {}
            group_size = 0
        else:
            for a in line.strip():
                group_answers[a] = group_answers.get(a, 0) + 1
            group_size += 1

    yield(total_part1 + len(group_answers))
    yield(total_part2 + sum(map(lambda a: group_answers[a] == group_size, group_answers)))

aoc.run(puzzles)
