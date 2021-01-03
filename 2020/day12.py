#!/usr/bin/python3

import aoc

import numpy as np

def puzzles(input_lines, **extra_args):
    direction_coeff = { "N": [0,1], "S": [0,-1], "E": [1,0], "W": [-1,0] }
    forward_coeff = [ [0,1], [1,0], [0,-1], [-1,0] ]

    pos_part1 = np.array([0, 0])
    pos_part2 = np.array([0, 0])
    heading = 90
    waypoint = np.array([10, 1])

    for line in input_lines:
        action, value = line[0], int(line[1:])

        if action in 'NSEW':
            pos_part1 += np.multiply(direction_coeff[action], value)
            waypoint += np.multiply(direction_coeff[action], value)
        elif action == 'F':
            pos_part1 += np.multiply(forward_coeff[heading//90], value)
            pos_part2 += np.multiply(waypoint, value)
        elif value == 180:
            heading = (heading + value) % 360
            waypoint *= -1
        elif value != 0:
            heading = (heading + value*(1 if action=='R' else -1)) % 360
            waypoint = waypoint[::-1] * ([1,-1] if line in [ 'R90', 'L270' ] else [-1,1])

    yield(sum(map(abs, pos_part1)))
    yield(sum(map(abs, pos_part2)))

aoc.run(puzzles)
