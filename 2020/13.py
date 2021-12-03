#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def find_next(buses, departures, ts, period, next_bus):
    next_ts = ts
    while True:
        next_ts += period
        for bus in [ buses[i] for i in range(buses.index(next_bus)+1) ]:
            if (next_ts+departures[bus]) % bus != 0:
                break
        else:
            break
    return(next_ts if next_bus == buses[-1] else find_next(buses, departures, next_ts, period*next_bus, buses[buses.index(next_bus)+1]))
    
def puzzles(input_lines, **extra_args):
    earliest = int(input_lines[0])
    buses = []
    departures = {}
    for t,bus in [ [t,int(b)] for t,b in enumerate(input_lines[1].split(",")) if b != "x" ]:
        buses.append(bus)
        departures[bus] = t

    if earliest == 0:
        yield(None)
    else:
        min_delay = best_bus = None
        for bus in buses:
            delay = bus - earliest % bus
            if min_delay is None or delay<min_delay:
                min_delay = delay
                best_bus = bus

        yield(min_delay*best_bus)

    yield(find_next(buses, departures, 0, buses[0], buses[1])) 

aoc.run(puzzles)
