#!/usr/bin/python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def run_prog(prog):
    eip = 0

    while prog[eip] != 99:
        if prog[eip] == 1:
            prog[prog[eip+3]] = prog[prog[eip+1]] + prog[prog[eip+2]]
            eip += 4
        elif prog[eip] == 2:
            prog[prog[eip+3]] = prog[prog[eip+1]] * prog[prog[eip+2]]
            eip += 4
        else:
            raise ValueError("Bad opcode %d at %d" % (prog[eip], eip))

def puzzles(input_lines, **extra_args):
    prog = [ int(v) for v in input_lines[0].split(",") ]

    answer1_prog = prog[:]
    if not extra_args['sample']:
        answer1_prog[1] = 12
        answer1_prog[2] = 2

    run_prog(answer1_prog)
    yield(answer1_prog[0])

    if extra_args['skip2']:
        yield(None)

    for noun in range(0,100):
        for verb in range(0,100):
            answer2_prog = prog[:]
            answer2_prog[1] = noun
            answer2_prog[2] = verb
            run_prog(answer2_prog)
            if answer2_prog[0] == 19690720:
                yield(noun*100+verb)

aoc.run(puzzles, samples = { 1: [ 3500, None ] })
