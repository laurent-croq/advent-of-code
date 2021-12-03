#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def solve_puzzle(input_lines, **extra_args):
    posX = 0
    posY = 0
    posY_answer2 = 0

    for cmd, value in [ line.split(" ") for line in input_lines ]:
        if cmd == "forward":
            posX += int(value)
            posY_answer2 += int(value) * posY
        elif cmd == "up":
            posY -= int(value)
        elif cmd == "down":
            posY += int(value)
    
    yield(posX*posY)
    yield(posX*posY_answer2)

aoc.run(solve_puzzle, { 1: [ 150, 900 ] } )
