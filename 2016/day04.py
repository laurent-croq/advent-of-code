#!/usr/bin/python3

import aoc

import re
def puzzles(input_lines, **extra_args):
    answer1 = 0
    answer2 = None

    for room in input_lines:
        m = re.match(r'(.*)-(\d+)\[(.*)\]', room)

        if m.group(3) == "".join(list(sorted(set(m.group(1))-{'-'}, key=lambda l: (-m.group(1).count(l), l))))[:5]:
            answer1 += int(m.group(2))
            real_name = "".join(" " if l=="-" else chr(ord('a')+(ord(l)-ord('a')+int(m.group(2)))%26) for l in m.group(1))
            if real_name == "northpole object storage":
                answer2 = m.group(2)

        # Ugly one-liner based on itertools!
        # import itertools
        #answer1 += int(m.group(2)) * (m.group(3) == "".join([ l for og in sorted([ list(o) for l,o in itertools.groupby(list([ len(list(group)), letter ] for letter, group in itertools.groupby(sorted(m.group(1).replace("-", ""))) ), key=lambda lo: lo[0]) ], key=lambda l: l[0][0], reverse=True) for _,l in sorted(og, key=lambda l: l[0], reverse=True) ] )[:5])
        # Equivalent to:
        #letter_occurrences = list([ len(list(group)), letter ] for letter, group in itertools.groupby(sorted(m.group(1).replace("-", ""))) )
        #this_checksum = ""
        #for occurrence_group in sorted([ list(occurrences) for letter, occurrences in itertools.groupby(letter_occurrences, key=lambda lo: lo[0]) ], key=lambda l: l[0][0], reverse=True):
        #    for _,letter in sorted(occurrence_group, key=lambda l: l[0], reverse=True):
        #        this_checksum+=letter
        #answer1 += int(m.group(2)) * (m.group(3) == this_checksum[:5])

    yield(answer1)
    yield(answer2)

aoc.run(puzzles)