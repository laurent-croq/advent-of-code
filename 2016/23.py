#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import re
from copy import deepcopy

def run(prog, regs):
    idx = 0
    while idx in range(len(prog)):
        if idx >= 16:            
            print("@%02d = %s (%s)" % (idx, prog[idx], " ".join("%s=%d" % (r, regs[r]) for r in regs)))
        if prog[idx][0] == "cpy":
            try:
                regs[prog[idx][2]] = int(regs.get(prog[idx][1], prog[idx][1]))
            except:
                pass
        elif prog[idx][0] == "inc":
            regs[prog[idx][1]] += 1
        elif prog[idx][0] == "dec":
            regs[prog[idx][1]] -= 1
        elif prog[idx][0] == "jnz" and int(regs.get(prog[idx][1], prog[idx][1])) != 0:
            idx += int(regs.get(prog[idx][2], prog[idx][2]))-1
        elif prog[idx][0] == "tgl":
            target = idx + int(regs.get(prog[idx][1], prog[idx][1]))
            if target in range(0, len(prog)):
                print("toggling %d" % target)
                if len(prog[target]) == 2:
                    prog[target][0] = "dec" if prog[target][0] == "inc" else "inc"
                else:
                    prog[target][0] = "cpy" if prog[target][0] == "jnz" else "jnz"
            else:
                print("Target of toggling is unreachable: %d" % target)
                
        idx+=1

def puzzles(input_lines, **extra_args):
    prog = [ line.split() for line in input_lines ]

    regs = { "a": 7, "b": 0, "c": 0, "d": 0 }
    run(deepcopy(prog), regs)

    yield(regs['a'])

    regs = { "a": 12, "b": 0, "c": 0, "d": 0 }
    run(deepcopy(prog), regs)

    yield(regs['a'])
    #80133408 = Too low...

aoc.run(puzzles)
