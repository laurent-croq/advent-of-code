#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import hashlib

def repeated_triplet(key):
    for i in range(len(key)-2):
        if key[i] == key[i+1] == key[i+2]:
            return(key[i])
    return(None)

def get_hash(salt, idx, repeat=0):
    h = hashlib.md5((salt+str(idx)).encode('utf-8')).hexdigest()
    for _ in range(repeat):
        h = hashlib.md5(h.encode('utf-8')).hexdigest()
    return(h)
    
def next1000_ok(salt, idx, c, repeat=0):
    for i in range(idx, idx+1000):
        if c*5 in get_hash(salt, i, repeat=repeat):
            return(True)
    return(False)

def puzzles(input_lines, **extra_args):
    salt = input_lines[0]
    
    idx = 0
    valid_indices = []
    while len(valid_indices)<64:
        this_key = get_hash(salt, idx)
        c = repeated_triplet(this_key)
        if c is not None and next1000_ok(salt, idx+1, c):
            valid_indices.append(idx)
        idx+=1

    yield(valid_indices[-1])

    idx = 0
    valid_indices = []
    while len(valid_indices)<64:
        this_key = get_hash(salt, idx, repeat=2016)
        c = repeated_triplet(this_key)
        if c is not None and next1000_ok(salt, idx+1, c, repeat=2016):
            print("Found", idx)
            valid_indices.append(idx)
        idx+=1

    yield(None)

aoc.run(puzzles)
