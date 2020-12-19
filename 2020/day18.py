#!/usr/bin/python3

import os, sys
sys.path.insert(1, os.getcwd()+"/..")
import aoc
puzzle_lines = aoc.load_puzzle_input()

formulas = []
formulas.extend([ line.replace(" ", "") for line in puzzle_lines ])

def matching_parenthesis(formula, pos):
    while formula[pos] != ')':
        if formula[pos] == '(':
            pos = matching_parenthesis(formula, pos+1)
        pos += 1
    return(pos)

def compute_part1(formula):
    try:
        op = formula.rindex("+")
        return(compute_part1(formula[:op]) + int(formula[op+1:]))
    except:
        pass

    try:
        op = formula.rindex("*")
        return(compute_part1(formula[:op]) * int(formula[op+1:]))
    except:
        pass

    return(int(formula))
    
import math
def compute_part2(formula):
    return(math.prod([ 1 ] + [ sum([ int(i) for i in additions.split("+") ]) for additions in formula.split("*") ]))
    
def solve_formula(formula, compute_func):
    try:
        idx_open = formula.index("(")
        idx_close = matching_parenthesis(formula, idx_open+1)
        return( solve_formula(formula[:idx_open] + str(solve_formula(formula[idx_open+1:idx_close], compute_func)) + formula[idx_close+1:], compute_func) )
    except:
        return(compute_func(formula))

print("answer1 = %d" % sum(solve_formula(f, compute_part1) for f in formulas))
print("answer2 = %d" % sum(solve_formula(f, compute_part2) for f in formulas))
