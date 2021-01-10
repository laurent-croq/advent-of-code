#!/usr/bin/python3.8

import aoc

def get_strongest(components, pins, get_longest=False):
    longest, strongest = 0, 0
    for component in [ c for c in components if pins in c ]:
        strength,length = tuple(map(sum, zip((sum(component), 1), get_strongest(set(components).difference([component]), component[0] if component[1]==pins else component[1], get_longest))))
        if get_longest:
            if length > longest or length == longest and strength > strongest:
                longest = length
                strongest = strength
        elif strength > strongest:
            strongest = strength
        
    return(strongest, longest)

def puzzles(input_lines, **extra_args):
    components = [ (int(c[0]), int(c[1])) for c in [ line.split("/") for line in input_lines ] ]
    
    yield(get_strongest(components, 0)[0])
    yield(get_strongest(components, 0, get_longest=True)[0])

aoc.run(puzzles)
