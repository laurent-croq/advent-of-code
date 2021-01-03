#!/usr/bin/python3

import aoc

def run(prog, regs):
    idx = 0
    while idx in range(len(prog)):
        if prog[idx][0] == "cpy":
            regs[prog[idx][2]] = int(regs.get(prog[idx][1], prog[idx][1]))
        elif prog[idx][0] == "inc":
            regs[prog[idx][1]] += 1
        elif prog[idx][0] == "dec":
            regs[prog[idx][1]] -= 1
        elif prog[idx][0] == "jnz" and int(regs.get(prog[idx][1], prog[idx][1])) != 0:
            idx += int(regs.get(prog[idx][2], prog[idx][2]))-1
        idx+=1
    return(regs['a'])

def puzzles(input_lines, **extra_args):
    prog = [ line.split() for line in input_lines ]

    yield(run(prog, { "a": 0, "b": 0, "c": 0, "d": 0 }))
    yield(run(prog, { "a": 0, "b": 0, "c": 1, "d": 0 }))

aoc.run(puzzles)