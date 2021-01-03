#!/usr/bin/python3

import aoc

from collections import deque

def puzzles(input_lines, **extra_args):
    forward = int(input_lines[0])

    buffer = [0]
    pos = 0
    for i in range(int(extra_args.get("n1", 2017))):
        buffer.insert((pos+forward)%len(buffer)+1, i+1)
        pos = (pos+forward)%(len(buffer)-1)+1
    yield(buffer[(pos+1)%len(buffer)])

    buffer = deque([0])
    for i in range(int(extra_args.get("n2", 50_000_000))):
        buffer.rotate(-forward)
        buffer.append(i+1)
    yield(buffer[buffer.index(0) + 1])

aoc.run(puzzles)