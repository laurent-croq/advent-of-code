#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import re

def is_valid(v, ranges):
    for r,r2 in [ [r,r2] for r in ranges for r2 in r ]:
        if v in range(r2[0], r2[1]+1):
            return(True)
    return(False)

def puzzles(input_lines, **extra_args):
    valid_ranges = []
    my_ticket = None
    nearby_tickets = []
    ranges_names = []

    for line in input_lines:
        m = re.search(r'(.*): (\d+)-(\d+) or (\d+)-(\d+)', line)
        if m is not None:
            valid_ranges.append([ [ int(m.group(2)), int(m.group(3)) ], [ int(m.group(4)), int(m.group(5)) ] ])
            ranges_names.append(m.group(1))
        else:
            try:
                ticket = [ int(n) for n in line.split(",") ]
            except ValueError:
                continue

            if my_ticket is None:
                my_ticket = ticket
            else:
                nearby_tickets.append(ticket)

    good_nearby_tickets = []
    error_rate = 0

    for t in nearby_tickets:
        for v in t:
            if not is_valid(v, valid_ranges):
                error_rate += v
                break
        else:
            good_nearby_tickets.append(t)

    yield(error_rate)

    final_good_ranges = [ [ i for i in range(len(valid_ranges))] for _ in valid_ranges ]
    good_ranges = [ [] for _ in valid_ranges ]

    for t in good_nearby_tickets:
        for v_idx,v in enumerate(t):
            this_good_range = []
            for r_idx,r in enumerate(valid_ranges):
                if is_valid(v, [ r ]) and r_idx not in good_ranges[v_idx]:
                    this_good_range.append(r_idx)
            final_good_ranges[v_idx] = list(set(final_good_ranges[v_idx]) & set(this_good_range)) 

    ordered_ranges = [ -1 for _ in valid_ranges ]
    for idx,r in sorted([ [ idx,r] for idx,r in enumerate(final_good_ranges) ], key=lambda v: len(v[1])):
        for v in r:
            if v not in ordered_ranges:
                ordered_ranges[idx] = v

    answer2 = 1
    for idx, r in [ idx_r for idx_r in enumerate(ordered_ranges) if ranges_names[idx_r[1]][0:len("departure ")] == "departure " ]:
        answer2 *= my_ticket[idx]

    yield(answer2)

aoc.run(puzzles)
