#!/usr/bin/python3

import aoc
puzzle_lines = aoc.read_puzzle_input()

import re

highest_seat_id = 0
seat_list = [ 0 ] * 2**(7+3)

for seat in puzzle_lines:
    seat_id = int("0b"+re.sub("[BR]", "1", re.sub("[FL]", "0", seat)), 2)
    highest_seat_id = max(highest_seat_id, seat_id)
    seat_list[seat_id] = 1

print("answer1 = %d" % highest_seat_id)

for seat_id in [ r*8+c for r in range(1, 2**7-1) for c in range(1, 2**3-1) ]:
    if seat_list[seat_id] == 0 and seat_list[seat_id-1] + seat_list[seat_id+1] == 2:
        print("answer2 = %d" % seat_id)
