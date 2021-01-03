#!/usr/bin/python3

import aoc

from heapq import heappop, heappush
from copy import deepcopy

def apply(state, boss_damage=0, spell=None):
    print("%s turn with %s (spell=%s)" % ("Player" if boss_damage==0 else "Boss", state, spell))
    has_shield = state['effects'][0]>0
    for e in [ e for e in range(3) if state['effects'][e] > 0 ]:
        state['effects'][e] -= 1
        if e == 1:
            state['boss'] -= 3
        elif e == 2:
            state['mana'] += 101

    if state['boss'] <= 0:
        print("You win")
        return

    if boss_damage>0:
        state['hits'] -= max(1, boss_damage-7*has_shield)
        if state['hits'] <= 0:
            print("You loose")
            return
    else:
        state['total_mana'] += (53,73,113,173,229)[spell]
        if spell == 0:
            state['boss'] -= 4
        elif spell == 1:
            state['boss'] -= 2
            state['hits'] += 2
        elif spell == 2:
            state['effects'][0] = 6
        elif spell == 3:
            state['effects'][1] = 6
        elif spell == 4:
            state['effects'][2] = 5

    print("  - leaving with %s (%d spent)" % (state, state['total_mana']))

def play_game(input_lines, part2=False):
    initial_state = { "hits": 50, "mana": 500, "effects": [ 0, 0, 0 ] }
    #initial_state = { "hits": 10, "mana": 250, "effects": [ 0, 0, 0 ] }
    initial_state["boss"] = int(input_lines[0].split()[2])
    boss_damage = int(input_lines[1].split()[1])

    history = []
    turns = []

    heappush(turns, (0, initial_state["boss"], 0, initial_state, []))
    total_turns = 0
    while True:
        total_mana_used, _, _, state, previous = heappop(turns)

        state['hits'] -= part2
        if state["hits"] <= 0:
            continue

        if state in history:
            continue
        history.append(state)

        # Applying effects before player turn
        for e in [ e for e in range(3) if state['effects'][e] > 0 ]:
            state['effects'][e] -= 1
            if e == 1:
                state['boss'] -= 3
            elif e == 2:
                state['mana'] += 101

        if state["boss"] <= 0:
            # Player wins
            return(total_mana_used)
        
        # Choosing a spell
        total_turns += 1
        for spell in [ i for i in range(5) if i<2 or state['effects'][i-2] == 0 ]:
            spell_cost = (53,73,113,173,229)[spell]
            if spell_cost > state['mana']:
                continue

            # Applying spell
            new_state = deepcopy(state)
            new_state['mana'] -= spell_cost
            if spell == 0:
                new_state['boss'] -= 4
            elif spell == 1:
                new_state['boss'] -= 2
                new_state['hits'] += 2
            elif spell == 2:
                new_state['effects'][0] = 6
            elif spell == 3:
                new_state['effects'][1] = 6
            elif spell == 4:
                new_state['effects'][2] = 5

            # Applying effects before boss turn
            new_state['hits'] -= max(1, boss_damage-7*(new_state['effects'][0]>0))
            for e in [ e for e in range(3) if new_state['effects'][e] > 0 ]:
                new_state['effects'][e] -= 1
                if e == 1:
                    new_state['boss'] -= 3
                elif e == 2:
                    new_state['mana'] += 101

            # Boss looses by poison effect
            if new_state['boss'] <= 0:
                return(total_mana_used + spell_cost)

            if new_state['hits'] > 0:
                heappush(turns, (total_mana_used+spell_cost, state['boss'], total_turns, new_state, previous+[spell]))

#    print("Winning with: %s" % previous)
#    state = deepcopy(initial_state)
#    state['total_mana'] = 0
#    for s in previous:
#        apply(state, spell=s)
#        apply(state, boss_damage=boss_damage)
#    return(total_mana_used)

def puzzles(input_lines, **extra_args):

    yield(play_game(input_lines))
    yield(play_game(input_lines, part2 = True))

aoc.run(puzzles)