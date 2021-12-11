#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc
import itertools

def do_flash(energy, flashed, x0, y0):
    total_flashes = 1
    flashed[y0][x0] = True
    energy[y0][x0] = 0
    for dx,dy in [ [dx,dy] for dx in range(-1,2) for dy in range(-1,2) ]:
        if x0+dx in (0,11) or y0+dy in (0,11) or flashed[y0+dy][x0+dx]:
            continue

        energy[y0+dy][x0+dx] += 1
        if energy[y0+dy][x0+dx] > 9:
            total_flashes += do_flash(energy, flashed, x0+dx, y0+dy)

    return(total_flashes)

def run_step(energy, flashed = None):
    if flashed is None:
        flashed = [ [False]*len(energy[0]) for _ in range(len(energy)) ]

    for x,y in [ [x,y] for x in range(1,11) for y in range(1,11) ]:
        energy[y][x] += 1

    total_flashes = 0
    for x,y in [ [x,y] for x in range(1,11) for y in range(1,11) if not flashed[y][x] ]:
        if energy[y][x] > 9:
            energy[y][x] = 0
            total_flashes += do_flash(energy, flashed, x, y)
    
    return(total_flashes)

def solve_puzzle(input_lines, **extra_args):
    answer1 = 0

    energy = [ [0]*12 ]
    for line in input_lines:
        energy.append([0] + [ int(n) for n in line ] + [0])

    energy.append([ [0]*12 ])

    for step in itertools.count(1):
        answer1 += run_step(energy)
        if step == 100:
            yield answer1

        if sum([ sum(line[1:11]) for line in energy[1:11] ]) == 0:
            yield step

aoc.run(solve_puzzle, samples = { 1:[1656,195] })
