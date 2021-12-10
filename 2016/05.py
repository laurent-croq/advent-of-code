#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import hashlib

def puzzles(input_lines, **extra_args):
    idx = 0
    password1 = ""
    password2 = "        "
    while len(password1) < 8 or password2.count(" ") > 0:
        this_hash = hashlib.md5((input_lines[0]+str(idx)).encode('utf-8')).hexdigest()
        if this_hash[:5] == "00000":
            if len(password1) < 8:
                password1 += this_hash[5]
                if len(password1) == 8:
                    yield(password1)
        
            if password2.count(" ") > 0 and this_hash[5] in "01234567" and password2[int(this_hash[5])] == " ":
                password2 = password2[:int(this_hash[5])] + this_hash[6] + password2[int(this_hash[5])+1:]
                if password2.count(" ") == 0:
                    yield(password2)
                    return
        idx+=1

aoc.run(puzzles, samples = { 1: [ "18f47a30", "05ace8e3" ] })
