#!/usr/bin/python3

import aoc

def distance(pos):
    pos = [ abs(pos[0]), abs(pos[1]) ]
    return(pos[1] if pos[1]>=2*pos[0] else int(pos[0]+pos[1]/2))

def puzzles(input_lines, **extra_args):
    pos = [0,0]
    answer_part2 = 0
    for move in input_lines[0].split(','):
        if move == "s":
            pos[0] -= 1
        elif move == "n":
            pos[0] += 1
        elif move == "ne":
            pos[0] += .5
            pos[1] += 1
        elif move == "nw":
            pos[0] += .5
            pos[1] -= 1
        elif move == "se":
            pos[0] -= .5
            pos[1] += 1
        elif move == "sw":
            pos[0] -= .5
            pos[1] -= 1

        answer_part2 = max(answer_part2, distance(pos))

    yield(distance(pos))
    yield(answer_part2)

aoc.run(puzzles)