#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import re

def swap_position(password, instruction):
    m = re.match(r'swap position (\d+) with position (\d+)', instruction)
    if m is None:
        return(password)
    c = password[int(m.group(1))]
    password[int(m.group(1))] = password[int(m.group(2))]
    password[int(m.group(2))] = c
    return(password)

def swap_letter(password, instruction):
    m = re.match(r'swap letter (.) with letter (.)', instruction)
    if m is None:
        return(password)
    s = "".join(password).replace(m.group(1), "#")
    s = s.replace(m.group(2), m.group(1))
    return(list(s.replace("#", m.group(2))))

def rotate_direction(password, instruction, reverse=False):
    m = re.match(r'rotate (left|right) (\d+) step', instruction)
    if m is None:
        return(password)
    if m.group(1) == "left" and not reverse or m.group(1) == "right" and reverse:
        return(password[int(m.group(2)):] + password[:int(m.group(2))])
    else:
        return(password[-int(m.group(2)):] + password[:-int(m.group(2))])

def rotate_based(password, instruction, reverse=False):
    m = re.match(r'rotate based on position of letter (.)', instruction)
    if m is None:
        return(password)
    pos = password.index(m.group(1))
    shift = (1, 1, 6, 2, 7, 3, 8, 4)[pos] if reverse else -pos-1-(pos>=4)
    return(password[shift:] + password[:shift])

def reverse_positions(password, instruction):
    m = re.match(r'reverse positions (\d+) through (\d+)', instruction)
    if m is None:
        return(password)
    return(password[:int(m.group(1))] + password[int(m.group(1)):int(m.group(2))+1][::-1] + password[int(m.group(2))+1:])

def move_position(password, instruction, reverse=False):
    m = re.match(r'move position (\d+) to position (\d+)', instruction)
    if m is None:
        return(password)
    c = password.pop(int(m.group( 2-(reverse == False) )))
    password.insert(int(m.group(2-reverse)), c)
    return(password)

def puzzles(input_lines, **extra_args):
    password = list(extra_args.get("part1", "abcdefgh"))

    for instruction in input_lines:
        password = swap_position(password, instruction)
        password = swap_letter(password, instruction)
        password = rotate_direction(password, instruction)
        password = rotate_based(password, instruction)
        password = reverse_positions(password, instruction)
        password = move_position(password, instruction)

    yield("".join(password))

    password = list(extra_args.get("part2", "fbgdceah"))

    for instruction in input_lines[::-1]:
        password = swap_position(password, instruction)
        password = swap_letter(password, instruction)
        password = rotate_direction(password, instruction, reverse=True)
        password = rotate_based(password, instruction, reverse=True)
        password = reverse_positions(password, instruction)
        password = move_position(password, instruction, reverse=True)
        #print("%s after %s" % ("".join(password), instruction))

    yield("".join(password))

aoc.run(puzzles)
