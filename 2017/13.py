#!/usr/bin/python3

import aoc

from itertools import cycle

def valid_ts(depth, width):
    ts = -depth%((width-1)*2)
    pos = 0
    while True:
        if pos != 0:
            yield(ts)
        pos = (pos+1)%((width-1)*2)
        ts+=1

def puzzles(input_lines, **extra_args):
    depths = dict( [ int(d), { "range": int(r), "pos": 0, "way": 1 } ] for d, r in [ line.split(": ") for line in input_lines ])

    severity = 0
    ts = 0
    while ts <= max(depths):
        for d in depths:
            if d == ts and depths[d]["pos"] == 0:
                severity += d*depths[d]["range"]
            depths[d]["pos"] += depths[d]["way"]
            if depths[d]['pos'] in (0, depths[d]['range']-1):
                depths[d]['way'] *= -1
        ts += 1

    yield(severity)

    depth_valid_ts = [ valid_ts(d, depths[d]['range']) for d in sorted(depths)]
    states = [ next(depth_valid_ts[i]) for i in range(len(depth_valid_ts)) ]
    while min(states) != max(states):
        for idx in range(len(states)):
            while states[idx] < max(states):
                states[idx] = next(depth_valid_ts[idx])

    # To be optimized: 5 minutes to get the answer
    yield(states[0])

aoc.run(puzzles)