#!/usr/bin/python3

import aoc

import re

def puzzles(input_lines, **extra_args):
    seats = {}

    for seat in input_lines:
        seats[int("0b"+re.sub("[BR]", "1", re.sub("[FL]", "0", seat)), 2)] = True
    
    yield(max(seats))

    for seat_id in [ r*8+c for r in range(1, 2**7-1) for c in range(1, 2**3-1) ]:
        if not(seats.get(seat_id, False)) and seats.get(seat_id-1, False) & seats.get(seat_id+1, False):
            yield(seat_id)
            return
    
    yield(None)

aoc.run(puzzles, samples = { 1: [357,None] })
