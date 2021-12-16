#!/usr/bin/env python3.8

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc, math

def parse_bitstring(bitstring):

    packet = { 'version': int(bitstring[0:3], 2), 'type_id': int(bitstring[3:6], 2), 'inner': [], 'size': 6 }
    packet['sum_version'] = packet['version']

    if packet['type_id'] == 4:
        pos = 6
        packet['value'] = int(bitstring[pos+1:pos+5], 2)
        while bitstring[pos] == "1":
            pos += 5
            packet['value'] = (packet['value']<<4) | int(bitstring[pos+1:pos+5], 2)
        packet['size'] = pos+5
    else:
        nb_size = 11 if bitstring[6] == '1' else 15
        packet['size'] += 1 + nb_size 
        pos = 7 + nb_size

        nb = int(bitstring[7:7+nb_size], 2)
        while nb > 0:
            inner_packet = parse_bitstring(bitstring[pos:])
            pos += inner_packet['size']
            packet['size'] += inner_packet['size']
            packet['sum_version'] += inner_packet['sum_version']
            packet['inner'].append(inner_packet)

            nb -= 1 if bitstring[6] == '1' else inner_packet['size']

        if packet['type_id'] == 0:
            packet['value'] = sum(p['value'] for p in packet['inner'])
        elif packet['type_id'] == 1:
            packet['value'] = math.prod(p['value'] for p in packet['inner'])
        elif packet['type_id'] == 2:
            packet['value'] = min(p['value'] for p in packet['inner'])
        elif packet['type_id'] == 3:
            packet['value'] = max(p['value'] for p in packet['inner'])
        elif packet['type_id'] == 5:
            packet['value'] = 1 if packet['inner'][0]['value'] > packet['inner'][1]['value'] else 0
        elif packet['type_id'] == 6:
            packet['value'] = 1 if packet['inner'][0]['value'] < packet['inner'][1]['value'] else 0
        elif packet['type_id'] == 7:
            packet['value'] = 1 if (packet['inner'][0]['value'] == packet['inner'][1]['value']) else 0

    return packet

def solve_puzzle(input_lines, **extra_args):

    bitstring = "{0:b}".format(int(input_lines[0],16))
    bitstring = "00000000"[:(8-len(bitstring)%8)%8] + bitstring

    packet = parse_bitstring(bitstring)

    yield packet['sum_version']
    yield packet['value']

aoc.run(solve_puzzle, samples = { 1:[16,15], 2:[12,46], 3:[23,46], 4:[31,54], 5:[14,3], 6:[8,54], 7:[15,7], 8:[11,9], 9:[13,1], 10:[19,0], 11:[16,0], 12:[20,1] })
