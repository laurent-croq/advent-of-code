#!/usr/bin/python3

import aoc

import re

def can_contain_shiny_gold(content, bag):
    if len(content[bag]) == 0:
        return(False)
    elif "shiny gold" in content[bag]:
        return(True)
    else:
        return(any([can_contain_shiny_gold(content, inner) for inner in content[bag]]))

def total_bags(content, bag):
    return(1 + sum(content[bag][inner] * total_bags(content, inner) for inner in content[bag]))

def puzzles(input_lines):
    content = {}
    for line in input_lines:
        m = re.search(r'^(.*) bags contain (.*)\.$', line)
        bag = m.group(1)
        content[bag] = {}
        if m.group(2) != "no other bags":
            for inner in m.group(2).split(", "):
                m = re.search(r'^(\d+) (.*) bags?$', inner)
                content[bag][m.group(2)] = int(m.group(1))

    yield(sum(can_contain_shiny_gold(content, bag) for bag in content))
    yield(total_bags(content, "shiny gold")-1)

aoc.run(puzzles)
