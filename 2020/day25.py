#!/usr/bin/python3

import aoc

def puzzles(input_lines, **extra_args):
    card_public_key = int(input_lines[0])
    door_public_key = int(input_lines[1])

    subject = encryption_key = 1
    while subject != card_public_key:
        encryption_key = (encryption_key*door_public_key)%20201227
        subject = (subject*7)%20201227

    yield(encryption_key)
    yield(None)

aoc.run(puzzles)
