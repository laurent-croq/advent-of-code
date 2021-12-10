#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import re

def uncompressed_size1(line):
    m = re.match(r'(.*?)\((\d+)x(\d+)\)(.*)', line)
    if m is None:
        return(len(line))
    else:
        return(len(m.group(1)) + int(m.group(2))*int(m.group(3)) + uncompressed_size1(m.group(4)[int(m.group(2)):]))

def uncompressed_size2(line):
    m = re.match(r'(.*?)\((\d+)x(\d+)\)(.*)', line)
    if m is None:
        return(len(line))
    else:
        return(len(m.group(1)) + uncompressed_size2(m.group(4)[:int(m.group(2))])*int(m.group(3)) + uncompressed_size2(m.group(4)[int(m.group(2)):] ))

def puzzles(input_lines, **extra_args):
    answer1 = answer2 = 0
    for line in input_lines:
        answer1 += uncompressed_size1(line)
        answer2 += uncompressed_size2(line)
    
    yield(answer1)
    yield(answer2)

aoc.run(puzzles)
