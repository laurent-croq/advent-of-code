#!/usr/bin/python3

import aoc

def explore_from(pipes, prog):
    explore = [ prog ]
    explored = []
    while len(explore) > 0:
        for prog in pipes[explore.pop()]:
            if prog not in explored:
                explore.append(prog)
                explored.append(prog)
    return(set(explored))

def puzzles(input_lines, **extra_args):
    pipes = {}

    for prog, links in [ line.split(" <-> ") for line in input_lines ]:
        pipes[int(prog)] = [ int(p) for p in links.split(', ') ]

    explored = explore_from(pipes, 0)
    yield(len(explored))

    answer_part2 = 1
    while len(explored) < len(pipes):
        explored |= explore_from(pipes, list(set(pipes).difference(explored))[0])
        answer_part2 += 1

    yield(answer_part2)

aoc.run(puzzles)