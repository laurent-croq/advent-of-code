#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def rating(diag_report, CO2_filter, pos=0):

    total_1 = sum([ line[pos] for line in diag_report ])

    most_bit = int(total_1 > len(diag_report)//2 or len(diag_report)-total_1 == len(diag_report)//2)

    remain = [ line for line in diag_report if line[pos] == (CO2_filter ^ most_bit) ]

    return rating(remain, CO2_filter, pos+1) if len(remain) > 1 else int("".join(str(b) for b in remain[0]), 2)

def solve_puzzle(input_lines, **extra_args):

    diag_report = [ [ int(b) for b in line ] for line in input_lines ]

    gamma = 0
    for line in map(list, zip(*diag_report)):
        gamma = gamma*2 + (sum(line) // (len(line)//2))

    yield gamma * (2**(len(diag_report[0]))-1 - gamma)
    yield rating(diag_report, False) * rating(diag_report, True)

aoc.run(solve_puzzle)
