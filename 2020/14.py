#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import re

def adresses(addr, bits):
    return([ addr, addr|bits[0] ] if len(bits)==1 else sum([ [a, a|bits[0]] for a in adresses(addr, bits[1:]) ], []))

def puzzles(input_lines, **extra_args):
    memory = {}

    for line in input_lines:
        if line[0:4] == "mask":
            mask_and = int("0b"+re.sub("X", "1", line[7:]), 2)
            mask_or = int("0b"+re.sub("X", "0", line[7:]), 2)
        else:
            m = re.search(r'mem.(\d+). = (\d+)', line)
            memory[int(m.group(1))] = (int(m.group(2)) & mask_and) | mask_or

    yield(sum(memory[a] for a in memory))

    memory = {}

    for line in input_lines:
        if line[0:4] == "mask":
            mask_and = int("0b"+re.sub("X", "0", re.sub("0", "1", line[7:])), 2)
            mask_or = int("0b"+re.sub("X", "0", line[7:]), 2)
            floating_bits = [2**(len(line)-i-8) for i, b in enumerate(re.sub("X", "1", re.sub("[01]", "0", line[7:]))) if b == "1"]
        else:
            m = re.search(r'mem.(\d+). = (\d+)', line)
            for addr in adresses((int(m.group(1)) & mask_and) | mask_or, floating_bits):
                memory[addr] = int(m.group(2))

    yield(sum(memory[a] for a in memory))

aoc.run(puzzles)
