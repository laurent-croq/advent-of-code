#!/usr/bin/python3

import aoc
puzzle_lines = aoc.read_puzzle_input()

seats = list(map(lambda l: [False]+[ s=='L' for s in l ]+[False], puzzle_lines))
seats.insert(0, [False]*len(seats[0]))
seats.append(seats[0])

import copy

def new_seat_state1(occupied, x, y):
    s = sum(occupied[x+h][y+v] for h in range(-1,2) for v in range(-1,2)) - occupied[x][y]
    return(occupied[x][y] and s<4 or not occupied[x][y] and s==0)

def apply_rule(occupied, new_seat_state):
    new_occupied = copy.deepcopy(occupied)

    for i,j in [ [i,j] for i in range(1, len(seats)) for j in range(1, len(seats[i])) if seats[i][j] ]:
        new_occupied[i][j] = new_seat_state(occupied, i, j)

    return(new_occupied)

occupied = list( [False]*len(seats[0]) for i in range(len(seats)) )
while True:
    new_occupied = apply_rule(occupied, new_seat_state1)
    if new_occupied == occupied:
        break
    occupied = new_occupied

print("answser1 = %d" % sum(occupied[i][j] for i in range(1, len(seats)) for j in range(1, len(seats[0]))))