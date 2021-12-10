#!/usr/bin/python3.8

import aoc

from heapq import heappop,heappush
from itertools import groupby
from copy import deepcopy

def puzzles(input_lines, **extra_args):
    particles = []

    for line in input_lines:
        particles.append(dict([p, [ int(v) for v in coord[1:-1].split(",") ]] for p,coord in [ c.split("=") for c in line.split(", ") ]))
        particles[-1]["i"] = len(particles)-1
    
    longterm = []
    particles_part1 = deepcopy(particles)
    count = 0
    while True:
        count +=1
        distances = []
        for idx,particle in enumerate(particles_part1):
            particle["v"] = list(map(sum, zip(particle["v"], particle["a"])))
            particle["p"] = list(map(sum, zip(particle["p"], particle["v"])))
            heappush(distances, [ sum(abs(v) for v in particle["p"]), idx ])

        longterm.append(heappop(distances)[1])
        if len(longterm) == 1000:
            if min(longterm) == max(longterm):
                break
            longterm.pop(0)

    yield(particles_part1[longterm[0]]["i"])

    particles_part2 = deepcopy(particles)
    count = 0
    while True:
        for particle in particles_part2:
            particle["v"] = list(map(sum, zip(particle["v"], particle["a"])))
            particle["p"] = list(map(sum, zip(particle["p"], particle["v"])))

        total_removed = 0
        remove_parts = list(list(l[1]) for l in groupby(sorted(range(len(particles_part2)), key=lambda idx: particles_part2[idx]["p"]), key=lambda idx: particles_part2[idx]["p"]) )
        for idx in sorted(sum([l for l in remove_parts if len(l)>1], []), reverse=True):
            total_removed += 1
            particles_part2.pop(idx)

        if total_removed == 0:
            count += 1
            if count == 10:
                break
        else:
            count = 0

    yield(len(particles_part2))

    # TODO to be refactored!!

aoc.run(puzzles)