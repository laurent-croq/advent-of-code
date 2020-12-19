#!/usr/bin/python3

import os, sys
sys.path.insert(1, os.getcwd()+"/..")
import aoc
puzzle_lines = aoc.load_puzzle_input()

earliest = int(puzzle_lines[0])
buses = []
departures = {}
for t,b in enumerate(puzzle_lines[1].split(",")):
    if b != "x":
        buses.append(int(b))
        departures[int(b)] = t

if earliest != 0:
    min_delay = None
    for b in buses:
        delay = b - earliest % b
        if min_delay is None or delay<min_delay:
            min_delay = delay
            best_bus = b

    print("answer1 = %d" % (min_delay*best_bus))

def find_next(ts, period, next_bus):
    next_ts = ts
    while True:
        next_ts += period
        for b in [ buses[i] for i in range(buses.index(next_bus)+1) ]:
            if (next_ts+departures[b]) % b != 0:
                break
        else:
            break
    
    return(next_ts if next_bus == buses[-1] else find_next(next_ts, period*next_bus, buses[buses.index(next_bus)+1]))

print("answer2 = %d" % find_next(0, buses[0], buses[1])) 
