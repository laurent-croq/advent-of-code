#!/usr/bin/env python3.8

import os,sys
from re import match
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc
from itertools import permutations, combinations
from copy import deepcopy

def apply_move(coord, rotate_x, invert_x, permute_axes, dx=0, dy=0, dz=0):
    new_coord = deepcopy(coord)
    for _ in range(rotate_x):
        new_coord = (new_coord[0],-new_coord[2],new_coord[1])

    new_coord = (invert_x*new_coord[0], new_coord[1], invert_x*new_coord[2])

    return (new_coord[permute_axes%3]+dx, new_coord[(1+permute_axes)%3]+dy, new_coord[(2+permute_axes)%3]+dz)

def resolve_scanner(scanners):
    for tested_scanner in [ s for s in scanners if 'moves' not in s ]:
        for relative_scanner in [ s for s in scanners if 'moves' in s and s not in tested_scanner['unrelated_scanners'] ]:
            relative_vectors = relative_scanner['vectors']
            tested_vectors = deepcopy(tested_scanner['vectors'])

            for rotate_x in range(4):
                for invert_x in (1, -1):
                    for permute_axes in (0, 1, -1):
                        matching_vectors = set(relative_vectors) & set(tested_vectors)
                        matching_beacons = set(relative_vectors[v][0] for v in matching_vectors) | set(relative_vectors[v][1] for v in matching_vectors)
                        if len(matching_beacons) >= 12:
                            reference_vector = matching_vectors.pop()
                            relative_coord = relative_scanner['beacons'][relative_vectors[reference_vector][0]]
                            tested_coord = apply_move(tested_scanner['beacons'][tested_vectors[reference_vector][0]], rotate_x, invert_x, permute_axes)
                            tested_scanner['moves'] = [ (rotate_x, invert_x, permute_axes, *map(lambda c: c[1]-c[0], zip(tested_coord, relative_coord))) ] + relative_scanner['moves']
                            return
                        tested_vectors = dict( [tuple((k[1],k[2],k[0])), v] for k,v in tested_vectors.items() )
                    tested_vectors = dict( [tuple((-k[0],k[1],-k[2])), v] for k,v in tested_vectors.items() )
                tested_vectors = dict( [tuple((k[0],-k[2],k[1])), v] for k,v in tested_vectors.items() )
            
            tested_scanner['unrelated_scanners'].append(relative_scanner)

def solve_puzzle(input_lines, **extra_args):
    scanners = []

    new_scanner = { "beacons": [], "vectors": {}, "unrelated_scanners": [] }
    for line in input_lines:
        if line == "":
            scanners.append(new_scanner)
            new_scanner = { "beacons": [], "vectors": {}, "unrelated_scanners": [] }
        elif line[:3] != "---":
            new_scanner['beacons'].append( tuple(int(s) for s in line.split(',') ))
    scanners.append(new_scanner)

    for scanner in scanners:
        for b0, b1 in permutations(range(len(scanner['beacons'])), 2):
            v = tuple(map(lambda coord: coord[1]-coord[0], zip(scanner['beacons'][b0], scanner['beacons'][b1])))
            scanner['vectors'][v] = (b0, b1)

    scanners[0]['moves'] = []
    while len([s for s in scanners if 'moves' not in s]) > 0:
        resolve_scanner(scanners)

    beacons = {}
    for scanner in scanners:
        for coord in scanner['beacons']:
            for move in scanner['moves']:
                coord = apply_move(coord, *move)
            beacons[coord] = True

    yield len(beacons)

    for scanner in scanners:
        scanner['center'] = (0,0,0)
        for move in scanner['moves']:
            scanner['center'] = apply_move(scanner['center'], *move)
            
    answer2 = 0
    for s0, s1 in combinations(range(len(scanners)), 2):
        answer2 = max(answer2, sum(map(lambda coord: abs(coord[1]-coord[0]), zip(scanners[s0]['center'], scanners[s1]['center']))))

    yield answer2

aoc.run(solve_puzzle, samples = { 1:[79,3621] })
