#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def solve_puzzle(input_lines, **extra_args):
    answer1 = 0
    answer2 = 0

    for signals,outputs in [ line.split(" | ") for line in input_lines ]:
        answer1 += sum([ len(seq) in [ 2,4,3,7 ] for seq in outputs.split(" ") ])

        total = [ [] for _ in range(8) ]
        letters = dict(zip("abcdefg", [0]*7))
        for pattern in signals.split(" "):
            total[len(pattern)].append(set(pattern))
            for l in pattern:
                letters[l] += 1

        a = list(total[3][0]-total[2][0])[0]
        b = [ l for l in letters if letters[l] == 6 ][0]
        d = list(total[4][0]-total[2][0]-set(b))[0]
        e = [ l for l in letters if letters[l] == 4 ][0]
        f = [ l for l in letters if letters[l] == 9 ][0]
        c = list(total[4][0]-set(f)-set(d)-set(b))[0]
        g = list(set("abcdefg")-set(a+b+c+d+e+f))[0]

        digits = [
                "".join(sorted(a+b+c+e+f+g)),
                "".join(sorted(c+f)),
                "".join(sorted(a+c+d+e+g)),
                "".join(sorted(a+c+d+f+g)),
                "".join(sorted(b+d+c+f)),
                "".join(sorted(a+b+d+f+g)),
                "".join(sorted(a+b+d+e+f+g)),
                "".join(sorted(a+c+f)),
                "".join(sorted(a+b+c+d+e+f+g)),
                "".join(sorted(a+b+c+d+f+g))
                ]

        numbers = [ "".join(sorted(n)) for n in outputs.split(" ") ]
        answer2 += int("".join([ str(digits.index(numbers[i])) for i in range(4)]))

    yield answer1
    yield answer2

aoc.run(solve_puzzle, samples = { 1: [ 26, 61229 ] } )
