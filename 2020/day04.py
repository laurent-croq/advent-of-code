#!/usr/bin/python3

import aoc

mandatory_fields = { 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid' }

def is_valid_value(value, pattern, min_v=None, max_v=None):
    import re
    m = re.search("^"+pattern+"$", value)
    if not m:
        return(False)

    return(True if min_v is None or (int(m.group(1))>=min_v and int(m.group(1))<=max_v) else False)

def is_valid_passport_part1(passport):
    return(set(passport).intersection(mandatory_fields) == mandatory_fields)

def is_valid_passport_part2(passport):
    for field in mandatory_fields:
        if field == 'byr':
            if not is_valid_value(passport[field], r'(\d{4})', 1920, 2002):
                return(False)
        elif field == 'iyr':
            if not is_valid_value(passport[field], r'(\d{4})', 2010, 2020):
                return(False)
        elif field == 'eyr':
            if not is_valid_value(passport[field], r'(\d{4})', 2020, 2030):
                return(False)
        elif field == 'hgt':
            if not is_valid_value(passport[field], r'(\d+)cm', 150, 193) and not is_valid_value(passport[field], r'(\d+)in', 59, 76):
                return(False)
        elif field == 'hcl':
            if not is_valid_value(passport[field], r'#[a-f0-9]{6}'):
                return(False)
        elif field == 'ecl':
            if not is_valid_value(passport[field], r'(amb|blu|brn|gry|grn|hzl|oth)'):
                return(False)
        elif field == 'pid':
            if not is_valid_value(passport[field], r'\d{9}'):
                return(False)
    return(True)

def puzzles(input_lines):
    valid_passports = []
    this_passport = {}
    for line in input_lines:
        if line == "":
            if is_valid_passport_part1(this_passport):
                valid_passports.append(this_passport)
            this_passport = {}
        else:
            for field, value in [ fv.split(':') for fv in line.split(' ') ]:
                this_passport[field] = value

    if is_valid_passport_part1(this_passport):
        valid_passports.append(this_passport)
    
    yield(len(valid_passports))
    yield(len([ p for p in valid_passports if is_valid_passport_part2(p) ]))

aoc.run(puzzles)
