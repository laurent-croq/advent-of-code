#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc
from copy import deepcopy
from itertools import permutations

def parse_sn_string(line):
    sn = [ None, None ]
    if line[1] == '[':
        sn[0], len_left = parse_sn_string(line[1:])
    else:
        sn[0] = int(line[1])
        len_left = 1
    
    if line[2+len_left] == '[':
        sn[1], len_right = parse_sn_string(line[2+len_left:])
    else:
        sn[1] = int(line[2+len_left])
        len_right = 1

    return sn, 3+len_left+len_right

def add_end_left(sn, number):
    if number == 0:
        return sn
    elif type(sn) == int:
        return sn+number
    else:
        return [ sn[0]+number if type(sn[0]) == int else add_end_left(sn[0], number), sn[1] ]

def add_end_right(sn, number):
    if number == 0:
        return sn
    elif type(sn) == int:
        return sn+number
    else:
        return [ sn[0], sn[1]+number if type(sn[1]) == int else [ sn[1][0], add_end_right(sn[1][1], number) ] ]

def explode_sn(sn, level=1):
    if level==5:
        return 0, True, sn[0], sn[1]

    if type(sn[0]) == list:
        sn[0], exploded, left_number, right_number = explode_sn(sn[0], level+1)
        if exploded:
            return [ sn[0], add_end_left(sn[1], right_number) ], True, left_number, 0

    if type(sn[1]) == list:
        sn[1], exploded, left_number, right_number = explode_sn(sn[1], level+1)
        if exploded:
            return [ add_end_right(sn[0], left_number), sn[1] ], True, 0, right_number

    return sn, False, None, None

def split_sn(sn):
    if type(sn[0]) == int:
        if sn[0] >= 10:
            sn[0] = [ sn[0]//2, sn[0]-sn[0]//2 ]
            return True
    elif split_sn(sn[0]):
        return True

    if type(sn[1]) == int:
        if sn[1] >= 10:
            sn[1] = [ sn[1]//2, sn[1]-sn[1]//2 ]
            return True
    elif split_sn(sn[1]):
        return True
    
    return False

def reduce_sn(sn):
    while True:
        exploded = True
        while exploded:
            sn, exploded, _, _ = explode_sn(sn)
        if not split_sn(sn):
            return(sn)

def sn_magnitude(sn):
    return 3*(sn[0] if type(sn[0]) == int else sn_magnitude(sn[0])) + 2*(sn[1] if type(sn[1]) == int else sn_magnitude(sn[1]))

def solve_puzzle(input_lines, **extra_args):
    sn_numbers = [ parse_sn_string(line)[0] for line in input_lines ]

    sn = deepcopy(sn_numbers[0])
    for next_sn in deepcopy(sn_numbers[1:]):
        sn = reduce_sn([sn, next_sn])
    
    yield sn_magnitude(sn)
    yield max([ sn_magnitude(reduce_sn([deepcopy(sn_a), deepcopy(sn_b)])) for sn_a, sn_b in permutations(sn_numbers, 2) ])

aoc.run(solve_puzzle, samples = { 1:[4140,3993]})
