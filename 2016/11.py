#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import re, itertools, copy

def shortest_path(state, history, total=0):
    #print("Testing %s" % state)
    elements = state['elements']
    if state in history or total>100:
        #print("Already tested")
        return(None)
    history.append(state)
    if state['elevator'] == 4 and sum(map(sum, [ elements[e] for e in elements ])) == 2*4*len(elements):
        print("Found")
        return(0)

    for e in [ e for e in elements if elements[e][0] != elements[e][1] ]:
        if len([ e2 for e2 in elements if elements[e2][0] == elements[e][1] ]) > 0:
            return(None)

    min_path = None
    candidates = [ [e,i] for e in elements for i in range(2) if elements[e][i] == state['elevator'] ]
#    print("Candidates: %s" % candidates)
    for choices in [ [c] for c in candidates ] + list(itertools.combinations(candidates, 2)):
        for next_floor in [ state['elevator']+i for i in [1,-1] if state['elevator']+i in range(1,5) ]:
            new_state = copy.deepcopy(state)
            new_state['elevator'] = next_floor
#            print("On floor %d: trying to move %s on floor %d" % (state['elevator'], str(choices), next_floor))
            for e,t in choices:
                new_state['elements'][e][t] = next_floor
            res = shortest_path(new_state, history, total+1)
            if res is not None:
                min_path = 1+res if min_path is None else min(min_path, 1+res)

    return(min_path)

def puzzles(input_lines, **extra_args):
    state = { "elevator": 1, "elements": {} }
    for line in input_lines:
        m = re.match(r'The (.*) floor contains (.*)\.', line)
        floor = [ None, "first", "second", "third", "fourth"].index(m.group(1))
        if m.group(2) == "nothing relevant":
            continue
        for element, type in [ re.sub("^(and )?a ", "", re.sub("-compatible", "", e)).split() for e in re.sub(r"([^,]) and a", r"\1, and a", m.group(2)).split(", ") ]:
            if state["elements"].get(element, None) is None:
                state["elements"][element] = [ None, None ]
            state["elements"][element][0 if type == "generator" else 1] = floor
    
    print(state)
    history = []

    yield(shortest_path(state, history))

    yield(None)

aoc.run(puzzles)
