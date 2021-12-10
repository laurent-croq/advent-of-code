#!/usr/bin/python3

import aoc

def perform_dance(programs, moves, count=1):
    programs = [ c for c in programs ]
    for _ in range(count):
        for move in moves:
            if move[0] == "s":
                programs = programs[-int(move[1][0]):] + programs[:-int(move[1][0])]
            elif move[0] == "x":
                programs[int(move[1][0])], programs[int(move[1][1])] = programs[int(move[1][1])], programs[int(move[1][0])]
            elif move[0] == "p":
                i1, i2 = programs.index(move[1][0]), programs.index(move[1][1])
                p1, p2 = programs[i1], programs[i2]
                programs[i1] = p2
                programs[i2] = p1
    return("".join(programs))

def puzzles(input_lines, **extra_args):
    moves = [ [ line[0], line[1:].split("/") ] for line in input_lines[0].split(",") ]

    programs = "abcdefghijklmnop"[:int(extra_args.get('n',16))]
    initial_programs = programs[:]

    yield(perform_dance(programs, moves))

    for i in range(1_000_000_000):
        programs = perform_dance(programs, moves)
        if programs == initial_programs:
            yield(perform_dance(programs, moves, 1_000_000_000%(i+1)))
            break

aoc.run(puzzles)