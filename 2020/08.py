#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import re,copy

def run(prog, running_part1=False):
    idx = 0
    acc = 0
    passed = [False] * len(prog)
    while True:
        if idx == len(prog):
            return(acc)
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

def puzzles(input_lines, **extra_args):
    prog = []
    for line in input_lines:
        m = re.search(r'^(nop|acc|jmp) (.\d+)$', line)
        prog.append([ m.group(1), int(m.group(2)) ])

    yield(run(prog, True))

    for i in [ i for i in range(len(prog)) if prog[i][0] != "acc" ]:
        new_prog = copy.deepcopy(prog)
        new_prog[i][0] = "jmp" if prog[i][0] == "nop" else "nop"

        acc = run(new_prog)
        if acc is not None:
            yield(acc)
            return
            
    yield(None)

aoc.run(puzzles)
