#!/usr/bin/python3

import aoc
puzzle_lines = aoc.load_puzzle_input()

import re

content = {}
for line in puzzle_lines:
    m = re.search(r'^(.*) bags contain (.*)\.$', line)
    bag = m.group(1)
    content[bag] = {}
    if m.group(2) != "no other bags":
        for inner in m.group(2).split(", "):
            m = re.search(r'^(\d+) (.*) bags?$', inner)
            content[bag][m.group(2)] = int(m.group(1))

def can_contain_shiny_gold(bag):
    if len(content[bag]) == 0:
        return(False)
    elif "shiny gold" in content[bag]:
        return(True)
    else:
        return(any([can_contain_shiny_gold(inner) for inner in content[bag]]))

print("answer1 = %d" % sum(can_contain_shiny_gold(bag) for bag in content))

def total_bags(bag):
    return(1 + sum(content[bag][inner] * total_bags(inner) for inner in content[bag]))

print("answer2 = %d" % (total_bags("shiny gold")-1))
