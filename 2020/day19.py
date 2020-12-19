#!/usr/bin/python3

import aoc
puzzle_lines = aoc.read_puzzle_input()

rules = []
messages = []

import re
for line in puzzle_lines:
    m = re.match(r'(\d+): (.*)', line)
    if m is not None:
        idx = int(m.group(1))
        for _ in range(len(rules), idx+1):
            rules.append([])
        rules[idx] = m.group(2)[1] if m.group(2)[0] == '"' else [ [ int(n) for n in subrule.split(' ') ] for subrule in m.group(2).split(" | ") ]
    elif len(line) > 0:
        messages.append(line)

def check_msg(msg, remain):
    if msg == "":
        return(msg if len(remain) == 0 else None)

    for idx, rule in enumerate([ rules[i] for i in remain ]):
        if type(rule) == str:
            if msg[0] != rule:
                return(None)
            else:
                msg = msg[1:]
                if msg == "":
                    return("" if idx == len(remain)-1 else None)
        else:
            for subrule in rule:
                res = check_msg(msg, subrule + remain[idx+1:])
                if res is not None:
                    return(res)
            return(None)

    return(msg)

print("answer1 = %d" % sum([ check_msg(m, [0]) == "" for m in messages ]))

total_part2 = 0
for msg in messages:
    msg = check_msg(msg, [ 42 ])
    if msg is None:
        continue

    total_42=1
    remain = check_msg(msg, [ 42 ])
    while remain != None:
        msg = remain
        remain = check_msg(msg, [ 42 ])
        total_42 += 1

    total_31=1
    msg = check_msg(msg, [ 31 ])
    while msg != None and msg != "":
        msg = check_msg(msg, [ 31 ])
        total_31 += 1

    if msg == "" and total_42>total_31:
        total_part2 += 1

print("answer2 = %d" % total_part2)
