#!/usr/bin/python3.8

import aoc

import re

def puzzles(input_lines, **extra_args):
    states = {}
    initial_state = None
    current_state = None
    current_value = None
    total_loops = None

    for line in input_lines:
        m = re.match(r"Begin in state (.)", line)
        if m is not None:
            initial_state = m.group(1)
            continue
        m = re.match(r"Perform a diagnostic checksum after (\d+) steps.", line)
        if m is not None:
            total_loops = int(m.group(1))
            continue
        m = re.match(r"In state (.):", line)
        if m is not None:
            states[m.group(1)] = { "value": [None,None], "move": [None,None], "state": [None,None] }
            current_state = states[m.group(1)]
            continue
        m = re.match(r"  If the current value is (\d):", line)
        if m is not None:
            current_value = int(m.group(1))
            continue
        m = re.match(r"    - Write the value (\d)", line)
        if m is not None:
            current_state["value"][current_value] = int(m.group(1))
            continue
        m = re.match(r"    - Move one slot to the (left|right)", line)
        if m is not None:
            current_state["move"][current_value] = 1 if m.group(1) == "right" else -1
            continue
        m = re.match(r"    - Continue with state (.)", line)
        if m is not None:
            current_state["state"][current_value] = m.group(1)
            continue
        if line != "":
            raise ValueError("No match for %s" % line)

    tape = {}
    pos = 0
    current_state = states[initial_state]
    for i in range(int(extra_args.get("n", total_loops))):
        current_value = tape.get(pos, 0)
        tape[pos] = current_state["value"][current_value]
        pos += current_state["move"][current_value]
        current_state = states[current_state["state"][current_value]]

    yield(sum(tape.values()))
    yield(None)

aoc.run(puzzles)
