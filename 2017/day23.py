#!/usr/bin/python3.8

import aoc

def run_prog(prog, regs):
    total_mul = 0
    idx = 0
    loop = 0
    while idx in range(0, len(prog)):
        instruction,arg1,arg2 = prog[idx] + [None]*(3-len(prog[idx]))
        value = int(regs.get(arg2, 0 if arg2 is None else arg2))
        if instruction == "set":
            regs[arg1] = value
        elif instruction == "sub":
            regs[arg1] = regs.get(arg1, 0) - value
        elif instruction == "mul":
            regs[arg1] = regs.get(arg1, 0) * value
            total_mul += 1
        elif instruction == "jnz" and int(regs.get(arg1, arg1)) != 0:
            idx += value - 1
        idx += 1
    return(total_mul)

def puzzles(input_lines, **extra_args):
    prog = [ line.split() for line in input_lines ]

    yield(run_prog(prog, dict([ c, 0 ] for c in "abcdefgh")))

    answer_part2 = 0
    for b in range(int(prog[0][2])*int(prog[4][2])-int(prog[5][2]), int(prog[0][2])*int(prog[4][2])-int(prog[5][2])-int(prog[7][2])+1, -int(prog[30][2])):
        for d in range(2,b):
            if b%d == 0:
                answer_part2 += 1
                break

    yield(answer_part2)

aoc.run(puzzles)