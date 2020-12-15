#!/usr/bin/python3

import aoc
puzzle_lines = aoc.load_puzzle_input()

puzzle_numbers = [ int(n) for n in puzzle_lines[0].split(',') ]

def solve(puzzle_numbers, max_turn):
    previous = {}
    last_seen = {}
    for i,n in enumerate(puzzle_numbers):
        last_seen[n] = i+1

    last_one = puzzle_numbers[-1]
    turn = len(puzzle_numbers)

    while turn < max_turn:
        next_one = last_seen[last_one]-previous[last_one] if last_one in previous else 0
        if next_one in last_seen:
            previous[next_one] = last_seen[next_one]

        turn += 1
        last_seen[next_one] = turn
        last_one = next_one
    
    return(last_one)

print("answer1 = %d" % solve(puzzle_numbers, 2020))
print("answer2 = %d" % solve(puzzle_numbers, 30000000))
