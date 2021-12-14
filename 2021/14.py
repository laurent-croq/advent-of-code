#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def solve_puzzle(input_lines, **extra_args):

    initial_polymer = input_lines[0]

    occurrences = {}
    rules = {}
    for seq,atom in [ line.split(" -> ") for line in input_lines[2:]]:
        rules[seq] = atom
        occurrences[atom] = initial_polymer.count(atom)
    
    current = polymer = { "atom": initial_polymer[0], "next": None }
    for atom in initial_polymer[1:]:
        current['next'] = { "atom": atom, 'next': None }
        current = current['next']

    for step in range(40):
        current = polymer
        while current['next'] is not None:
            next_seq = current['next']
            current['next'] = { 'atom': rules[current['atom'] + current['next']['atom']], 'next': next_seq }
            occurrences[current['next']['atom']] += 1
            current = next_seq
        #print(occurrences)

        if step == 9:
            yield max(occurrences.values()) - min(occurrences.values())

    yield max(occurrences.values()) - min(occurrences.values())

aoc.run(solve_puzzle, samples = { 1: [1588,2188189693529] })
