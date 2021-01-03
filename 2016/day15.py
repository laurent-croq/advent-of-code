#!/usr/bin/python3

import aoc

import re

def dump(discs, start):
    max_print = 100
    print( (" "*start + "V")[:max_print])
    for d in discs:
        s = " " * ((d[0]-d[1])%d[0])
        for _ in range(100):
            s += "*" + " " * (d[0]-1)
        print(s[:max_print])

def puzzles(input_lines, **extra_args):
    discs = []

    for line in input_lines:
        m = re.match(r'Disc #\d+ has (\d+) positions; at time=(\d+), it is at position (\d+)', line)
        discs.append( ( int(m.group(1)), (int(m.group(3))-int(m.group(2)))%int(m.group(1)) ) )

    start = (discs[0][0]-discs[0][1]-1) % discs[0][0]
    period = discs[0][0]

    #print("disc0 = %d/%d @ t0" % (discs[0][1], discs[0][0]))
    #print("Starting at t=%d" % start)
    #dump(discs[:1], start)

    discs += [ (11,0) ]
    for i in range(1, len(discs)):
        #print("disc%d = %d/%d @ t0" % (i, discs[i][1], discs[i][0]))
        while (start+discs[i][1]+1+i) % discs[i][0] != 0:
            start += period
        period *= discs[i][0]
        #print("\nNow starting at %d with new period %d" % (start, period))
        #dump(discs[:1+i], start)
        if i == len(discs)-2:
            yield(start)

    yield(start)

aoc.run(puzzles)