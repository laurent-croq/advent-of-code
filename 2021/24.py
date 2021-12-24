#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def MONAD_step(w, z, div_z, add_x, add_y):
    return (z // div_z) * (25 * ((z % 26 + add_x) != w) + 1) + (w + add_y) * ((z % 26 + add_x) != w)

def solve_puzzle(input_lines, **extra_args):

    b_values = {
        "div_z": [ int(input_lines[4  + i*18][6:]) for i in range(14) ],
        "add_x": [ int(input_lines[5  + i*18][6:]) for i in range(14) ],
        "add_y": [ int(input_lines[15 + i*18][6:]) for i in range(14) ]
    }

    valid_w_z = [ [] for _ in range(14) ] + [ [ (None, 0) ] ]
    for i in range(13,-1,-1):
        for z in set(s[1] for s in valid_w_z[i+1]):
            for new_z in range(z*b_values['div_z'][i], (z+1)*b_values['div_z'][i]):
                w = new_z%26+b_values['add_x'][i]
                if w in range(1,10):
                    valid_w_z[i].append((w, new_z))

            for w in range(1,10):
                new_z_26 = ((z-w-b_values['add_y'][i])*b_values['div_z'][i])
                if new_z_26 % 26 == 0:
                    valid_w_z[i].append((w, new_z_26//26))

    z = 0
    answer1 = ""
    for i in range(14):
        w = max(s[0] for s in valid_w_z[i] if s[1] == z)
        answer1 += str(w)
        z = MONAD_step(w, z, b_values['div_z'][i], b_values['add_x'][i], b_values['add_y'][i])

    yield answer1

    z = 0
    answer2 = ""
    for i in range(14):
        w = min(s[0] for s in valid_w_z[i] if s[1] == z)
        answer2 += str(w)
        z = MONAD_step(w, z,b_values['div_z'][i], b_values['add_x'][i], b_values['add_y'][i])

    yield answer2

aoc.run(solve_puzzle, samples = { })
