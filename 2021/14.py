#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def diff_most_least(pair_counts, last_atom):
    atoms = { last_atom: 1 }
    for a,count in [ (pair[0],pair_counts[pair]) for pair in pair_counts]:
        atoms[a] = atoms.get(a,0) + count

    return max(atoms.values()) - min(atoms.values())

def solve_puzzle(input_lines, **extra_args):

    initial_polymer = input_lines[0]
    new_atom = dict([ line.split(" -> ") for line in input_lines[2:]])
    
    pair_counts = dict(zip(new_atom, [0]*len(new_atom)))
    for pair in [ initial_polymer[i:i+2] for i in range(len(initial_polymer)-1) ]:
        pair_counts[pair] += 1

    for step in range(40):
        if step == 10:
            yield diff_most_least(pair_counts, initial_polymer[-1])
            
        new_pair_counts = dict(zip(new_atom, [0]*len(new_atom)))
        for pair in pair_counts:
            new_pair_counts[pair[0]+new_atom[pair]] += pair_counts[pair]
            new_pair_counts[new_atom[pair]+pair[1]] += pair_counts[pair]
        pair_counts = new_pair_counts

    yield diff_most_least(pair_counts, initial_polymer[-1])

aoc.run(solve_puzzle, samples = { 1: [1588,2188189693529] })
