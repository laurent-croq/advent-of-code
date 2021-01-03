#!/usr/bin/python3

import aoc

def puzzles(input_lines, **extra_args):
    row = "." + input_lines[0] + "."
    total_safe = row.count(".")-2

    for idx in range(int(extra_args.get("part2", 400000))-1):
        new_row = "."
        for i in range(1, len(row)-1):
            new_row += "^" if row[i-1:i+2] in ("^^.", ".^^", "^..", "..^") else "."
        new_row += "."
        row = new_row
        total_safe += row.count(".")-2
        if idx == int(extra_args.get("part1", 40))-2:
            yield(total_safe)

    yield(total_safe)

aoc.run(puzzles)