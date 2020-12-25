#!/usr/bin/python3

import os, sys
sys.path.insert(1, os.getcwd()+"/..")
import aoc
puzzle_lines = aoc.load_puzzle_input()

card_public_key = int(puzzle_lines[0])
door_public_key = int(puzzle_lines[1])

subject = encryption_key = 1
while subject != card_public_key:
    encryption_key = (encryption_key*door_public_key)%20201227
    subject = (subject*7)%20201227

print("answer1 = %d" % encryption_key)
