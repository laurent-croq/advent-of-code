#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def solve_puzzle(input_lines, **extra_args):
    answer1 = None
    answer2 = None

    read_points = True
    points = []
    folds = []
    for line in input_lines:
        if line == "":
            read_points = False
        elif read_points:
            points.append(tuple(map(int, line.split(","))))
        else:
            folds.append((line[11], int(line[13:])))

    paper = [ [False] * (max(list(map(list, zip(*points)))[0]) + 1) for _ in range(max(list(map(list, zip(*points)))[1]) + 1)]
    for x,y in points:
        paper[y][x] = True

    for way,pos in folds:
        if way == "x":
            for y in range(len(paper)):
                #for x in range(pos):
                #    paper[y][x] |= paper[y][len(paper[y])-x-1]
                #paper[y] = paper[y][:pos]
                paper[y] = tuple(map(lambda v: v[0]|v[1], zip(paper[y][:pos], paper[y][-1:-pos-1:-1])))
        else:
            #for x,y in [ (x,y) for y in range(pos) for x in range(len(paper[y])) ]:
            #    paper[y][x] |= paper[len(paper)-y-1][x]
            for y in range(len(paper)):
                paper[y] = tuple(map(lambda v: v[0]|v[1], zip(paper[y], paper[len(paper)-y-1])))
            paper = paper[:pos]

        if answer1 is None:
            answer1 = sum(sum(paper, ())) # sum([ sum(paper[y]) for y in range(len(paper)) ])

    for y in range(len(paper)):
        print("".join([ "X" if v else " " for v in paper[y]]))
    
    yield answer1
    yield answer2

aoc.run(solve_puzzle, samples = { 1: [17,None] })
