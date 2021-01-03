#!/usr/bin/python3

import aoc

def puzzles(input_lines, **extra_args):
    regs = {}
    answer_part2 = 0
    for reg, op, value, _, cond_reg, cond_op, cond_value in [ line.split() for line in input_lines ]:
        cond_result = None
        if cond_op == '>':
            cond_result = (regs.get(cond_reg, 0) > int(cond_value))
        elif cond_op == '<':
            cond_result = (regs.get(cond_reg, 0) < int(cond_value))
        elif cond_op == '>=':
            cond_result = (regs.get(cond_reg, 0) >= int(cond_value))
        elif cond_op == '<=':
            cond_result = (regs.get(cond_reg, 0) <= int(cond_value))
        elif cond_op == '==':
            cond_result = (regs.get(cond_reg, 0) == int(cond_value))
        elif cond_op == '!=':
            cond_result = (regs.get(cond_reg, 0) != int(cond_value))
   
        if cond_result:
            regs[reg] = regs.get(reg, 0) + int(value) * (1 if op == "inc" else -1)

        answer_part2 = max([answer_part2] + [regs[r] for r in regs])

    yield(max(regs[r] for r in regs))

    yield(answer_part2)

aoc.run(puzzles)