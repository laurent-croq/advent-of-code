#!/usr/bin/python3

import aoc

from math import prod

def puzzles(input_lines, **extra_args):
    maze = input_lines[:]

    direction = [1, 0]
    pos = [0, maze[0].index("|")]

    answer_part1 = ""
    answer_part2 = 0
    maze_height, maze_width = len(maze), len(maze[0])
    while True:
        new_pos = [ pos[0]+direction[0], pos[1]+direction[1] ]
        while new_pos[0] in range(maze_height) and new_pos[1] in range(maze_width):
            answer_part2 += 1
            pos = new_pos
            if maze[pos[0]][pos[1]] in ("+", " "):
                break
            if ord(maze[pos[0]][pos[1]]) in range(ord("A"), ord("Z")+1):
                answer_part1 += maze[pos[0]][pos[1]]
            new_pos = list(map(sum, zip(pos, direction)))

        if maze[pos[0]][pos[1]] == " ":
            break
        direction = [ direction[1], direction[0] ]
        if pos[0]+direction[0] not in range(maze_height) or maze[pos[0]+direction[0]][pos[1]+direction[1]] == " ":
            direction = list(map(lambda v: -v, direction))

    yield(answer_part1)
    yield(answer_part2)

aoc.run(puzzles)