#!/usr/bin/python3

import aoc

def puzzles(input_lines, **extra_args):
    input_digits = input_lines[0]
    answer1 = 0
    for i in range(len(input_digits)):
        answer1 += int(input_digits[i]) * (input_digits[i] == input_digits[0 if i==len(input_digits)-1 else i+1])
    
    yield(answer1)

    answer2 = 0
    for i in range(len(input_digits)//2):
        answer2 += 2 * int(input_digits[i]) * (input_digits[i] == input_digits[i+len(input_digits)//2])
    
    yield(answer2)

aoc.run(puzzles, samples = { 1: [3,0], 2: [4,4], 3:[9,6], 4:[0,4], 5:[0,12] })