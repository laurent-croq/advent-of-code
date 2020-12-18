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

import re
def compute_sum(op):
    try:
        idx_open = op.index("(")
        idx_close = find_matching(op[idx_open:])
        return( compute_sum(op[:idx_open] + str(compute_sum(op[idx_open+1:idx_open+idx_close])) + op[idx_open+idx_close+1:]) )
    except:
        pass

    m = re.match(r'(.*)([+*])(\d+)', op)
    if m is None:
        return(int(op))
    else:
        if m.group(2) == "+":
            return(compute_sum(m.group(1)) + int(m.group(3)))
        else:
            return(compute_sum(m.group(1)) * int(m.group(3)))
    
print("answer = %d" % sum(compute_sum(op) for op in operations))
