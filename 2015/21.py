#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import itertools
from heapq import heappush,heappop

weapons = {
    "Dagger":       { "cost": 8,  "damage": 4, "armor": 0 },
    "Shortsword":   { "cost": 10, "damage": 5, "armor": 0 },
    "Warhammer":    { "cost": 25, "damage": 6, "armor": 0 },
    "Longsword":    { "cost": 40, "damage": 7, "armor": 0 },
    "Greataxe":     { "cost": 74, "damage": 8, "armor": 0 }
}

armors = {
    "Leather":      { "cost": 13,  "damage": 0, "armor": 1 },
    "Chainmail":    { "cost": 31,  "damage": 0, "armor": 2 },
    "Splintmail":   { "cost": 53,  "damage": 0, "armor": 3 },
    "Bandedmail":   { "cost": 75,  "damage": 0, "armor": 4 },
    "Platemail":    { "cost": 102, "damage": 0, "armor": 5 }
}

rings = {
    "Damage +1":    { "cost": 25,  "damage": 1, "armor": 0 },
    "Damage +2":    { "cost": 50,  "damage": 2, "armor": 0 },
    "Damage +3":    { "cost": 100, "damage": 3, "armor": 0 },
    "Defense +1":   { "cost": 20,  "damage": 0, "armor": 1 },
    "Defense +2":   { "cost": 40,  "damage": 0, "armor": 2 },
    "Defense +3":   { "cost": 80,  "damage": 0, "armor": 3 }
}

all_items = { **weapons, **armors, **rings }

def player_wins_with(items, boss):
    players = [ { "hit": 100, "damage": 0, "armor": 0 }, boss.copy() ]

    for item in [ all_items[i] for i in items if i is not None ]:
        players[0]['damage'] += item['damage']
        players[0]['armor'] += item['armor']

    turn = 0
    while True:
        players[1-turn]['hit'] -= max(1, players[turn]['damage']-players[1-turn]['armor'])
        if players[1-turn]['hit'] <= 0:
            return(turn == 0)
        turn = 1-turn

def puzzles(input_lines, **extra_args):
    boss = {}
    boss["hit"] = int(input_lines[0].split()[2])
    boss["damage"] = int(input_lines[1].split()[1])
    boss["armor"] = int(input_lines[2].split()[1])

    all_possibilities = []
    for items in [ [w,a,*r] for w in weapons for a in list(armors)+[None] for r in list(itertools.combinations(rings,2)) + [ [r] for r in list(rings) ] + [[None]] ]:
        heappush(all_possibilities, (sum(item['cost'] for item in [ all_items[i] for i in items if i is not None ]), len(all_possibilities), items))

    possibilities = all_possibilities[:]
    for least_gold, _, items in [ heappop(possibilities) for _ in range(len(possibilities)) ]:
        if player_wins_with(items, boss):
            yield(least_gold)
            break

    possibilities = all_possibilities[:]
    for most_gold, _, items in [ heappop(possibilities) for _ in range(len(possibilities)) ][::-1]:
        if not player_wins_with(items, boss):
            yield(most_gold)
            break

aoc.run(puzzles)
