#!/usr/bin/python3.8

import aoc

def puzzles(input_lines, **extra_args):
    infected = {}
    for y,line in enumerate(input_lines):
        for x in [ x for x,c in enumerate(line) if c == "#" ]:
            infected[ (y,x) ] = 1

    carrier = (len(input_lines)//2,len(input_lines)//2)
    direction = (-1,0)
    total_infected = 0
    for _ in range(int(extra_args.get("n1", 10000))):
        direction = (direction[1]*infected.get(carrier, -1), direction[0]*-infected.get(carrier, -1))
        infected[carrier] = -infected.get(carrier, -1)
        total_infected += (infected[carrier] == 1)
        carrier = tuple(map(sum,zip(carrier,direction)))

    yield(total_infected)

    states = {}
    for y,line in enumerate(input_lines):
        for x in [ x for x,c in enumerate(line) if c == "#" ]:
            states[ (y,x) ] = "I"

    carrier = (len(input_lines)//2,len(input_lines)//2)
    direction = (-1,0)
    total_infected = 0
    for _ in range(int(extra_args.get("n2", 10000000))):
        if states.get(carrier, "C") == "I":
            direction = (direction[1], -direction[0])
        elif states.get(carrier, "C") == "C":
            direction = (-direction[1], direction[0])
        elif states.get(carrier, "C") == "F":
            direction = (-direction[0], -direction[1])
        states[carrier] = "WIFC"["CWIF".index(states.get(carrier, "C"))]
        total_infected += (states[carrier] == "I")
        carrier = tuple(map(sum,zip(carrier,direction)))

    yield(total_infected)

aoc.run(puzzles)
