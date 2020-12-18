#!/usr/bin/python3

import aoc
puzzle_lines = aoc.read_puzzle_input()

operations = []
for line in puzzle_lines:
    operations.append(line.replace(" ", ""))

def find_matching(op):
    x = 1
    while op[x] != ')':
        x += 1 if op[x] != '(' else 1+find_matching(op[x:])
    return(x)

def compute_sum(op):
    try:
        idx_open = op.index("(")
        idx_close = find_matching(op[idx_open:])
        return( compute_sum(op[:idx_open] + str(compute_sum(op[idx_open+1:idx_open+idx_close])) + op[idx_open+idx_close+1:]) )
    except:
        pass

    if len(op.split("*")) == 1:
        return(sum([ int(i) for i in op.split("+") ] ))

    res = 1
    for sub_op in op.split("*"):
        res *= compute_sum(sub_op)

    return(res)
    
print("answer = %d" % sum(compute_sum(op) for op in operations))
