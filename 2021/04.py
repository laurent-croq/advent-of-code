#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc
import re

def solve_puzzle(input_lines, **extra_args):
    answer1 = None
    answer2 = None

    numbers = [ int(n) for n in input_lines[0].split(",") ]

    boards = []
    number2boards = [ [] for _ in range(100) ]

    for i in range(2, len(input_lines), 6):
        new_board = []
        for j in range(i, i+5):
            new_board.append([ int(n) for n in re.sub(" +", ";", input_lines[j].strip()).split(";") ])
            for k,n in enumerate(new_board[-1]):
                number2boards[n].append([len(boards), k, (j-i)%6 ])

        boards.append(new_board)

    for number in numbers:
        for player,col,row in number2boards[number]:
            if boards[player] is None:
                continue

            boards[player][row][col] = None

            if sum(filter(None, boards[player][row])) == 0 or sum(filter(None, list(map(list, zip(*boards[player])))[col])) == 0:
                answer2 = number * sum( sum(filter(None, row)) for row in boards[player] )
                if answer1 is None:
                    answer1 = answer2

                boards[player] = None
    
    yield answer1
    yield answer2

aoc.run(solve_puzzle, samples = { 1: [ 4512, 1924 ] })
