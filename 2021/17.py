#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc, re

def solve_puzzle(input_lines, **extra_args):
    answer1 = 0
    answer2 = 0

    x_min, x_max, y_min, y_max = map(int, re.search(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', input_lines[0]).groups())

    for start_x_vel in range(1, 200):
        for y_vel in range(-200, 200):
            x_vel = start_x_vel
            x = y = max_high = 0
            while x <= x_max and y >= y_min:
                x += x_vel
                y += y_vel
                x_vel = max(0, x_vel-1)
                y_vel -= 1

                max_high = max(max_high, y)

                if y>=y_min and y<=y_max:
                    answer1 = max(answer1, max_high)

                    if x>=x_min and x<=x_max:
                        answer2 += 1
                        break

    yield answer1
    yield answer2

aoc.run(solve_puzzle, samples = { 1:[45,112] })
