#!/usr/bin/python3

import aoc

def puzzles(input_lines, **extra_args):
    banks = [ int(n) for n in input_lines[0].split() ]

    previous = []
    total_cycles = 0
    answer_part1 = None
    answer_part2 = None

    while True:
        if answer_part1 is None:
            if banks in previous:
                answer_part1 = total_cycles
                total_cycles = 0
                previous = banks[:]
            else:
                previous.append(banks[:])
        else:
            if banks == previous:
                answer_part2 = total_cycles
                break
        total_cycles+=1

        idx = banks.index(max(banks))
        total_blocks = banks[idx]
        banks[idx] = 0
        for i in range(len(banks)):
            banks[i] += total_blocks//len(banks)
        for i in range(total_blocks%len(banks)):
            banks[(idx+i+1)%len(banks)] += 1

    yield(answer_part1)
    yield(answer_part2)

aoc.run(puzzles)