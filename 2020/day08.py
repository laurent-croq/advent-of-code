#!/usr/bin/python3

import os, sys
sys.path.insert(1, os.getcwd()+"/..")
import aoc
puzzle_lines = aoc.load_puzzle_input()

import re

prog = []
for line in puzzle_lines:
    m = re.search(r'^(nop|acc|jmp) (.\d+)$', line)
    prog.append([ m.group(1), int(m.group(2)) ])

def run(prog, running_part1=False):
    idx = 0
    acc = 0
    passed = [False] * len(prog)
    while True:
        if idx == len(prog):
            return(acc)
        elif idx<0 or idx>len(prog):
            raise ValueError ("Out of range instruction #%d" % idx)
        elif passed[idx]:
            return(acc if running_part1 else None)

        passed[idx] = True
        if prog[idx][0] == "nop":
            idx += 1
        elif prog[idx][0] == "jmp":
            idx += prog[idx][1]
        elif prog[idx][0] == "acc":
            acc += prog[idx][1]
            idx += 1
        else:
            raise ValueError ("Unsupported instruction #%d: %s %d" % (idx, prog[idx][0], prog[idx][1]))

print("answer1 = %s" % run(prog, True))

import copy
for i in [ i for i in range(len(prog)) if prog[i][0] != "acc" ]:
    new_prog = copy.deepcopy(prog)
    new_prog[i][0] = "jmp" if prog[i][0] == "nop" else "nop"

    acc = run(new_prog)
    if acc is not None:
        print("answer2 = %s" % acc)
