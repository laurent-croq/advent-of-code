#!/usr/bin/python3

import os, sys
sys.path.insert(1, os.getcwd()+"/..")
import aoc
puzzle_lines = aoc.load_puzzle_input()

deck1 = []
deck2 = []
current_deck = deck1
for line in puzzle_lines:
    if line == "":
        current_deck = deck2
    elif line[-1] != ":":
        current_deck.append(int(line))

def play_game1(deck1, deck2):
    while len(deck1)>0 and len(deck2)>0:
        if deck1[0] > deck2[0]:
            deck1.append(deck1.pop(0))
            deck1.append(deck2.pop(0))
        else:
            deck2.append(deck2.pop(0))
            deck2.append(deck1.pop(0))

    return(deck1 if len(deck2) == 0 else deck2)

def play_game2(deck1, deck2, subgame=False):
    if subgame and max(deck1) > max(deck2):
        return(1)

    previous_rounds = []
    while len(deck1)>0 and len(deck2)>0:
        previous_rounds.append([deck1[:], deck2[:]])
        if [ deck1, deck2 ] in previous_rounds[:-1]:
            winner = 1
        elif len(deck1[1:]) >= deck1[0] and len(deck2[1:]) >= deck2[0]:
            winner = play_game2(deck1[1:1+deck1[0]], deck2[1:1+deck2[0]], subgame=True)
        else:
            winner = 1 if deck1[0] > deck2[0] else 2

        if winner == 1:
            deck1.append(deck1.pop(0))
            deck1.append(deck2.pop(0))
        else:
            deck2.append(deck2.pop(0))
            deck2.append(deck1.pop(0))

    if subgame:
        return(1 if len(deck2) == 0 else 2)
    else:
        return(deck1 if len(deck2) == 0 else deck2)

print("answer1 = %d" % sum(v*(i+1) for i,v in enumerate(play_game1(deck1[:], deck2[:])[::-1])))
print("answer2 = %d" % sum(v*(i+1) for i,v in enumerate(play_game2(deck1[:], deck2[:])[::-1])))
