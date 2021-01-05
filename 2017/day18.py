#!/usr/bin/python3

import aoc

def run_prog(pid, prog, idx, regs, queues, total_sent):
    total = 0
    while idx[pid] in range(0, len(prog)):
        instruction,arg1,arg2 = prog[idx[pid]] + [None]*(3-len(prog[idx[pid]]))
        value = int(regs[pid].get(arg2, 0 if arg2 is None else arg2))
        if instruction == "snd":
            queues[1-pid].insert(0, int(regs[pid].get(arg1, arg1)))
            total_sent[pid] += 1
        elif instruction == "rcv":
            if len(queues[pid]) == 0:
                return(total)
            regs[pid][arg1] = queues[pid].pop()
        elif instruction == "set":
            regs[pid][arg1] = value
        elif instruction == "add":
            regs[pid][arg1] = regs[pid].get(arg1, 0) + value
        elif instruction == "mul":
            regs[pid][arg1] = regs[pid].get(arg1, 0) * value
        elif instruction == "mod":
            regs[pid][arg1] = regs[pid].get(arg1, 0) % value
        elif instruction == "jgz" and int(regs[pid].get(arg1, arg1)) > 0:
            idx[pid] += value - 1
        idx[pid] += 1
        total += 1

def puzzles(input_lines, **extra_args):
    prog = [ line.split() for line in input_lines ]

    pos = 0
    regs = {}
    last_freq = None
    while pos in range(0, len(prog)):
        if prog[pos][0] == "snd":
            last_freq = regs[prog[pos][1]]
        elif prog[pos][0] == "set":
            regs[prog[pos][1]] = int(regs.get(prog[pos][2], prog[pos][2]))
        elif prog[pos][0] == "add":
            regs[prog[pos][1]] = regs.get(prog[pos][1], 0) + int(regs.get(prog[pos][2], prog[pos][2]))
        elif prog[pos][0] == "mul":
            regs[prog[pos][1]] = regs.get(prog[pos][1], 0) * int(regs.get(prog[pos][2], prog[pos][2]))
        elif prog[pos][0] == "mod":
            regs[prog[pos][1]] = regs.get(prog[pos][1], 0) % int(regs.get(prog[pos][2], prog[pos][2]))
        elif prog[pos][0] == "rcv" and regs[prog[pos][1]] != 0:
            yield(last_freq)
            break
        elif prog[pos][0] == "jgz" and regs[prog[pos][1]] > 0:
            pos += int(regs.get(prog[pos][2], prog[pos][2])) - 1
        pos += 1
    
    queues = [ [], [] ]
    regs = [ { "p": 0 }, { "p": 1 } ]
    idx = [ 0, 0 ]
    total_sent = [ 0, 0 ]
    while idx[0] in range(len(prog)) and idx[1] in range(len(prog)):
        if run_prog(0, prog, idx, regs, queues, total_sent) + run_prog(1, prog, idx, regs, queues, total_sent) == 0:
            break

    yield(total_sent[1])

aoc.run(puzzles)