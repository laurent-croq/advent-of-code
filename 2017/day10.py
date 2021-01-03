#!/usr/bin/python3

import aoc

from functools import reduce
from operator import xor

def knot_hash(numbers, lengths, count=1):
    skip = begin = 0
    for length in lengths * count:
        numbers = numbers[:length][::-1] + numbers[length:]
        numbers = numbers[(length+skip)%len(numbers):] + numbers[:(length+skip)%len(numbers)]
        begin = (begin-skip-length)%len(numbers)
        skip += 1
    return(numbers[begin:] + numbers[:begin])

def puzzles(input_lines, **extra_args):
    try:
        lengths = [ int(n) for n in input_lines[0].split(',') ]
        numbers = knot_hash(list(range(int(extra_args.get("n", 256)))), lengths)
        yield(numbers[0]*numbers[1])
    except:
        yield(None)

    lengths = [ ord(c) for c in input_lines[0] ] + [ 17, 31, 73, 47, 23 ]
    numbers = knot_hash(list(range(int(extra_args.get("n", 256)))), lengths, 64)
    yield("".join("%02x" % i for i in [ reduce(xor, block) for block in [ numbers[i:i+16] for i in range(0,256,16) ] ]))

aoc.run(puzzles)