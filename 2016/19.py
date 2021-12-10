#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def winner_part1_with_dict(total_elves):
    presents = dict([ i+1, i+1 ] for i in range(total_elves))
    neighbors = dict([i, i+1] for i in range(1, total_elves+1))
    neighbors[total_elves] = 1

    current = 1
    while len(neighbors) > 1:
        presents[current] += presents[neighbors[current]]
        delete_elf = neighbors[current]
        neighbors[current] = neighbors[delete_elf]
        del neighbors[delete_elf]
        current = neighbors[current]

    return(current)

def winner_part1_with_list(total_elves):
    presents = dict([ i+1, i+1 ] for i in range(total_elves))
    circle = [ i+1 for i in range(total_elves) ]

    while len(circle) > 1:
        new_circle = []
        for i in range(0, len(circle)-1, 2):
            presents[circle[i]] += presents[circle[i+1]]    
            new_circle.append(circle[i])
        if len(circle)%2 == 0:
            circle = new_circle
        else:
            presents[circle[len(circle)-1]] += presents[circle[0]]
            circle = new_circle[1:] + [ circle[len(circle)-1] ]

    return(circle[0])

def winner_part2_with_list(total_elves):
    # To be improved! (15 minutes to solve)
    presents = dict([ i+1, i+1 ] for i in range(total_elves))
    circle = [ i+1 for i in range(total_elves) ]

    current = 0
    while len(circle) > 1:
        #print("Circle is %s, current=%d" % (circle, current))
        target = (current+len(circle)//2)%len(circle)
        #print("- elf %d@%d steals presents of elf %d@%d" % (circle[current], current, circle[target], target))
        presents[circle[current]] += presents[circle[target]]
        circle.pop(target)
        current += current<target
        current %= len(circle)

    return(circle[0])

def puzzles(input_lines, **extra_args):
    total_elves = int(input_lines[0])

    yield(winner_part1_with_list(total_elves))
    yield(winner_part2_with_list(total_elves))

aoc.run(puzzles)
