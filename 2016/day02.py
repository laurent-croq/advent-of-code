#!/usr/bin/python3

import aoc

keypad_part1 = [
    "     ",
    " 123 ",
    " 456 ",
    " 789 ",
    "     "
]

keypad_part2 = [
    "       ",
    "   1   ",
    "  234  ",
    " 56789 ",
    "  ABC  ",
    "   D   ",
    "       "
]

def choose_key(keypad, current_key, instructions):
    directions = { "U": [-1,0], "D": [1,0], "L": [0,-1], "R": [0,1] }
    for i in instructions:
        next_key = [sum(c) for c in zip(current_key, directions[i])]
        if keypad[next_key[0]][next_key[1]] != " ":
            current_key[0], current_key[1] = next_key
    return(str(keypad[current_key[0]][current_key[1]]))

def puzzles(input_lines, **extra_args):
    code = ""
    current_key = [2, 2]
    for instructions in input_lines:
        code += choose_key(keypad_part1, current_key, instructions)

    yield(code)

    code = ""
    current_key = [3, 1]
    for instructions in input_lines:
        code += choose_key(keypad_part2, current_key, instructions)

    yield(code)

aoc.run(puzzles, samples = { 1: ["1985", "5DB3"] })