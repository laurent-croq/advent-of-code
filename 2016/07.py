#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import re

def is_abba(seq):
    for i in range(len(seq)-3):
        if seq[i]==seq[i+3] and seq[i+1]==seq[i+2] and seq[i]!=seq[i+1]:
            return(True)
    return(False)

def supports_tls(seq):
    found_abba = False
    while seq != "":
        if seq[0] == "[":
            if is_abba(seq[1:seq.index("]")]):
                return(False)
            seq = seq[seq.index("]")+1:]
        else:
            try:
                if is_abba(seq[:seq.index("[")]):
                    found_abba = True
                seq = seq[seq.index("["):]
            except:
                return(found_abba or is_abba(seq))

    return(found_abba)

def find_abas(seq, negate=False):
    abas = []
    for i in range(len(seq)-2):
        if seq[i]==seq[i+2] and seq[i]!=seq[i+1]:
            abas.append(seq[i+1]+seq[i]+seq[i+1] if negate else seq[i:i+3])
    return(abas)

def supports_ssl(seq):
    supernet_abas = []
    hypernet_abas = []

    while seq != "":
        if seq[0] == "[":
            hypernet_abas.extend(find_abas(seq[1:seq.index("]")], negate=True))
            seq = seq[seq.index("]")+1:]
        else:
            try:
                supernet_abas.extend(find_abas(seq[:seq.index("[")]))
                seq = seq[seq.index("["):]
            except:
                supernet_abas.extend(find_abas(seq))
                return(len(set(supernet_abas).intersection(hypernet_abas))>0)

    return(len(set(supernet_abas).intersection(hypernet_abas))>0)

def puzzles(input_lines, **extra_args):
    total_tls = 0
    total_ssl = 0
    for line in input_lines:
        total_tls += supports_tls(line)
        total_ssl += supports_ssl(line)
    
    yield(total_tls)
    yield(total_ssl)

aoc.run(puzzles)
