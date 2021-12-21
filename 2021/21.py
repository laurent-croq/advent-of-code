#!/usr/bin/env python3.8

import itertools
import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

def total_victories(player_A, player_B, current_universes=1):
    if player_B[1]>=21:
        return 0,current_universes

    total_A = total_B = 0
#    for move,combi in zip(range(2,9), (1,3,6,7,6,3,1)):
    for move,combi in ( (2,1), (3,3), (4,6), (5,7), (6,6), (7,3), (8,1) ):
        new_place = (player_A[0]+move)%10 + 1
        victories_B, victories_A = total_victories(player_B, (new_place, player_A[1]+new_place), current_universes*combi)
        total_A += victories_A
        total_B += victories_B
    
    return total_A, total_B

def solve_puzzle(input_lines, **extra_args):

    initial_place1 = int(input_lines[0].split(": ")[1])
    initial_place2 = int(input_lines[1].split(": ")[1])
    players = [ [initial_place1, 0], [initial_place2, 0] ]

#    turn = 0
#    dice = 1
#    for roll in itertools.count(3,3):
#        move = 0
#        for _ in range(3):
#            move += dice
#            dice = 1+dice%100
#        players[turn][0] = 1 + (players[turn][0]+move-1)%10
#        players[turn][1] += players[turn][0]
#        if players[turn][1] >= 1000:
#            break
#        turn = 1 - turn

    move = 0
    for dice,roll in zip(itertools.cycle(range(100)), itertools.count(1)):
        move = (0 if (roll-1)%3 == 0 else move) + dice + 1
        if roll%3 == 0:
            turn = ((roll-1)//3)%2
            players[turn][0] = 1 + (players[turn][0]+move-1)%10
            players[turn][1] += players[turn][0]
            if players[turn][1] >= 1000:
                break

    yield players[1-turn][1]*roll
    yield max(total_victories([initial_place1, 0], [initial_place2, 0]))

aoc.run(solve_puzzle, samples = { 1:[739785,444356092776315] })
