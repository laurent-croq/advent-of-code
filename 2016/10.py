#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import re

def puzzles(input_lines, **extra_args):
    bots = {}
    init_values = []
    outputs = {}

    for line in input_lines:
        m = re.match(r'value (\d+) goes to bot (\d+)', line)
        if m is not None:
            init_values.append([ int(m.group(1)), int(m.group(2)) ])
        else:
            m = re.match(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)', line)
            bots[int(m.group(1))] = { "values": [], "processed": False, "low": int(m.group(3)), "high": int(m.group(5)), "dest": [ m.group(2), m.group(4) ] }

    for v,b in init_values:
        bots[b]["values"].append(v)
    
    while True:
        processed = 0
        for bot in [ bots[b] for b in bots if len(bots[b]["values"])==2 and not bots[b]["processed"] ]:
            if bot["dest"][0] == "bot":
                bots[bot["low"]]["values"].append(min(bot["values"]))
            else:
                outputs[bot["low"]] = min(bot["values"])
            if bot["dest"][1] == "bot":
                bots[bot["high"]]["values"].append(max(bot["values"]))
            else:
                outputs[bot["high"]] = max(bot["values"])
            processed += 1
            bot["processed"] = True

        if processed == 0:
            break
    
    yield([ b for b in bots if set(bots[b]["values"]) == set([17,61]) ][0])
    yield(outputs[0]*outputs[1]*outputs[2])

aoc.run(puzzles)
