#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def get_checksum(data, disk_size):
    while len(data)<disk_size:
        data += "0" + "".join([ "0" if c=="1" else "1" for c in data[::-1] ])

    data = data[:disk_size]
    checksum = data[:]
    while len(checksum)%2 == 0:
        new_checksum = ""
        for a,b in [ (checksum[i], checksum[i+1]) for i in range(0, len(checksum)-1, 2) ]:
            new_checksum += "1" if a==b else "0"
        checksum = new_checksum

    return(checksum)    

def puzzles(input_lines, **extra_args):
    data = input_lines[0]

    yield(get_checksum(data, 272))
    yield(get_checksum(data, 35651584))

aoc.run(puzzles)
