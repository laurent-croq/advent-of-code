#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def print_image(image):
    for line in image:
        print("".join("#" if c == "1" else "." for c in line))

def expand_image(image, padding):
    for i in range(len(image)):
        image[i] = padding + image[i] + padding
    
    image.insert(0, padding*len(image[0]))
    image.append(padding*len(image[0]))

def solve_puzzle(input_lines, **extra_args):
    algo = "".join("1" if c=="#" else "0" for c in input_lines[0])
    image = list("".join("1" if c=="#" else "0" for c in line) for line in input_lines[2:])

    padding = "0"
    for _ in range(2):
        expand_image(image, padding)

    for step in range(50):
        padding = algo[int(padding*9,2)]

#        new_image = [ padding * len(image[0]) ]
#        for y in range(1, len(image)-1):
#            new_line = ""
#            for x in range(1, len(image[0])-1):
#                new_line += algo[int(image[y-1][x-1:x+2] + image[y][x-1:x+2] + image[y+1][x-1:x+2],2)]
#            new_image.append(padding + new_line + padding)
#        image = new_image + [ padding * len(image[0]) ]

        image = [ padding * len(image[0]) ] + \
                list(padding + "".join(algo[int(image[y-1][x-1:x+2] + image[y][x-1:x+2] + image[y+1][x-1:x+2],2)] for x in range(1, len(image[0])-1)) + padding for y in range(1, len(image)-1)) + \
                [ padding * len(image[0]) ]

        expand_image(image, padding)
        if step == 1:
            yield sum(line.count("1") for line in image)
    
    yield sum(line.count("1") for line in image)

aoc.run(solve_puzzle, samples = { 1:[35,3351] })
