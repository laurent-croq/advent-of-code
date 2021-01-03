#!/usr/bin/python3

import aoc

import re

def puzzles(input_lines, **extra_args):
    
    screen = [ [ False ] * 50 for _ in range(6) ]

    for line in input_lines:
        m = re.match(r'rect (\d+)x(\d+)', line)
        if m is not None:
            for y in range(int(m.group(2))):
                screen[y] = [ True ] * int(m.group(1)) + screen[y][int(m.group(1)):]
        else:
            m = re.match(r'rotate (row|column) .=(\d+) by (\d+)', line)
            if m.group(1) == "row":
                screen[int(m.group(2))] = screen[int(m.group(2))][-int(m.group(3)):]+screen[int(m.group(2))][:-int(m.group(3))]
            else:
                col = [ screen[y][int(m.group(2))] for y in range(len(screen)) ]
                for y in range(len(screen)):
                    screen[y][int(m.group(2))] = col[(y-int(m.group(3)))%len(screen)]
        
        print(line)
        for y in range(len(screen)):
            print("".join([ "#" if screen[y][x] else "." for x in range(len(screen[y])) ]))
        print("===")
    yield(sum(map(sum, screen)))
    yield(None)

aoc.run(puzzles)