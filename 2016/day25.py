#!/usr/bin/python3

import aoc

def run(prog, regs, max_print=80):
    idx = 0
    while idx in range(len(prog)) and max_print>0:
        if prog[idx][0] == "cpy":
            regs[prog[idx][2]] = int(regs.get(prog[idx][1], prog[idx][1]))
        elif prog[idx][0] == "inc":
            regs[prog[idx][1]] += 1
        elif prog[idx][0] == "dec":
            regs[prog[idx][1]] -= 1
        elif prog[idx][0] == "jnz" and int(regs.get(prog[idx][1], prog[idx][1])) != 0:
            idx += int(regs.get(prog[idx][2], prog[idx][2]))-1
        elif prog[idx][0] == "out":
            print("#" if int(regs.get(prog[idx][1], prog[idx][1])) == 1 else ".", end="")
            max_print -= 1
        idx+=1
    print("")

def puzzles(input_lines, **extra_args):
    prog = [ line.split() for line in input_lines ]

    base = int(prog[1][1]) * int(prog[2][1])
    answer_part1 = int("10"*len(bin(base)[2::2]),2)-base

    yield(answer_part1)
    run(prog, { "a": answer_part1, "b": 0, "c": 0, "d": 0 })
    yield(None)

aoc.run(puzzles)