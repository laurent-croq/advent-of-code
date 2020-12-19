#!/usr/bin/python3

import os, sys
sys.path.insert(1, os.getcwd()+"/..")
import aoc
puzzle_lines = aoc.load_puzzle_input()

import re

total_valid1 = 0
total_valid2 = 0
#for val1,val2,char,password in [ [ int(d[0]), int(d[1]), d[2], d[3] ] for line in puzzle_lines for d in [ re.sub(r"^(\d+)-(\d+) (\w): (\w*)", r"\1:\2:\3:\4", line).split(":") ] ]:
for line in puzzle_lines:
    for val1,val2,char,password in [ [ int(d[0]), int(d[1]), d[2], d[3] ] for d in [ re.sub(r"^(\d+)-(\d+) (\w): (\w*)", r"\1:\2:\3:\4", line).split(":") ] ]:
        c = password.count(char)
        if c>=val1 and c<=val2:
            total_valid1 += 1

        if (password[val1-1] == char) != (password[val2-1] == char):
            total_valid2 += 1

print("answer1 = %d" % total_valid1)
print("answer2 = %d" % total_valid2)

