#!/usr/bin/python3

import aoc

def puzzles(input_lines, **extra_args):
    pos_answer1 = [ 0, 0 ]
    pos_answer2 = None
    direction = [ 0, 1 ]
    previous_positions = [ pos_answer1 ]
    for instruction in input_lines[0].split(", "):
        direction = [ direction[1], -direction[0] ] if instruction[0] == 'R' else [ -direction[1], direction[0] ]
        for _ in range(int(instruction[1:])):
            pos_answer1 = list(map(sum, zip(pos_answer1, direction)))
            if pos_answer2 is None:
                if pos_answer1 in previous_positions:
                    pos_answer2 = pos_answer1
                else:
                    previous_positions.append(pos_answer1)
            
    yield(sum(map(abs,pos_answer1)))
    yield(sum(map(abs,pos_answer2)))

aoc.run(puzzles)