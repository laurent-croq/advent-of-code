#!/usr/bin/python3

import aoc
puzzle_lines = aoc.load_puzzle_input()

seats = list(map(lambda l: [False]+[ s=='L' for s in l ]+[False], puzzle_lines))
seats.insert(0, [False]*len(seats[0]))
seats.append(seats[0])

import copy

def new_seat_state1(occupied, x, y):
    s = sum(occupied[x+h][y+v] for h in range(-1,2) for v in range(-1,2)) - occupied[x][y]
    return(occupied[x][y] and s<4 or not occupied[x][y] and s==0)

def new_seat_state2(occupied, x, y):
    seen = 0
    for dx,dy in [ [dx,dy] for dx in range(-1,2) for dy in range(-1,2) if [dx,dy] != [0,0] ]:
        check_x = x+dx
        check_y = y+dy
        while check_x in range(len(seats)) and check_y in range(len(seats[0])) and not seats[check_x][check_y]:
            check_x += dx
            check_y += dy

        if check_x in range(len(seats)) and check_y in range(len(seats[0])) and occupied[check_x][check_y]:
            seen += 1
            if not occupied[x][y] or seen == 5:
                return(False)
    return(True)

def apply_rule(occupied, new_seat_state):
    new_occupied = copy.deepcopy(occupied)

    for i,j in [ [i,j] for i in range(1, len(seats)) for j in range(1, len(seats[i])) if seats[i][j] ]:
        new_occupied[i][j] = new_seat_state(occupied, i, j)

    return(new_occupied)

occupied = list( [False]*len(seats[0]) for _ in range(len(seats)) )
while True:
    new_occupied = apply_rule(occupied, new_seat_state1)
    if new_occupied == occupied:
        break
    occupied = new_occupied

print("answer1 = %d" % sum(sum(occupied, [])))

occupied = list( [False]*len(seats[0]) for i in range(len(seats)) )
while True:
    new_occupied = apply_rule(occupied, new_seat_state2)
    if new_occupied == occupied:
        break
    occupied = new_occupied

print("answer2 = %d" % sum(sum(occupied, [])))
