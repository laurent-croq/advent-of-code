#!/usr/bin/python3

import aoc

import re
from heapq import heappop,heappush

def puzzles(input_lines, **extra_args):
    rules = {}
    molecule = None
    for line in input_lines:
        m = re.match(r'(.*) => (.*)', line)
        if m is not None:
            rules[m.group(2)] = m.group(1)
        elif line != "":
            molecule = line

    trans = []
    heappush(trans, (len(molecule), 0, 0, molecule))
    previous = []
    total_iter = 0
    min_changes = 0
    while True:
        if len(trans) == 0:
            print("Not found...")
            exit(1)
        _,total_changes,_,current = heappop(trans)
        #print("Handling %s with %d changes" % (current, total_changes))
        if total_changes > min_changes:
            min_changes = total_changes
            print("Minimum changes = %d" % min_changes)

        if current == "e":
            break
        new_added = 0
        for r in sorted(rules, key=lambda p: len(rules[p])): #, reverse=True):
            (next_molecule, nb_changes) = re.subn(r, rules[r], current, 1)
            if next_molecule not in previous:
                total_iter +=1
                new_added +=1
                heappush(trans, (len(next_molecule), total_changes + nb_changes, total_iter, next_molecule))
                previous.append(next_molecule)
        if new_added == 0:
            print("No more change with %s" % current)

    yield(None)
    yield(total_changes)

aoc.run(puzzles)