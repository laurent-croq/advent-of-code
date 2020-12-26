#!/usr/bin/python3

import aoc
puzzle_lines = aoc.load_puzzle_input()

total_part1 = 0
total_part2 = 0

group_answers = {}
group_size = 0
for line in puzzle_lines:
    if line == "":
        total_part1 += len(group_answers)
        total_part2 += sum(map(lambda a: group_answers[a] == group_size, group_answers))
        #OR total_part2 += len([ a for a in group_answers if group_answers[a] == group_size ])
        group_answers = {}
        group_size = 0
    else:
        for a in line.strip():
            group_answers[a] = group_answers.get(a, 0) + 1
        group_size += 1

total_part1 += len(group_answers)
total_part2 += len([ a for a in group_answers if group_answers[a] == group_size ])

print("answer1 = %d" % total_part1)
print("answer2 = %d" % total_part2)
