#!/usr/bin/python3

import aoc
puzzle_numbers = [ int(n) for n in aoc.read_puzzle_input() ]

def is_XMAS_valid(idx):
    for i in range(idx-25,idx):
        if puzzle_numbers[idx]-puzzle_numbers[i] in puzzle_numbers[i:idx]:
            return(True)
    return(False)

for idx in range(25, len(puzzle_numbers)):
    if not is_XMAS_valid(idx):
        invalid_idx = idx
        invalid_number = puzzle_numbers[idx]
        print("answer1 = %d (at #%d)" % (invalid_number, invalid_idx))
        break

for idx in range(1, invalid_idx):
    for i in range(idx+1):
        this_set = [ n for n in puzzle_numbers[i:idx] ]
        if sum(this_set) == invalid_number:
            print("answer2 = %d (at #%d, sum of %d numbers)" % (min(this_set) + max(this_set), i, idx-i))

