#!/usr/bin/python3

import aoc

def is_XMAS_valid(numbers, idx):
    for i in range(idx-25,idx):
        if numbers[idx]-numbers[i] in numbers[i:idx]:
            return(True)
    return(False)

def puzzles(input_lines):
    numbers = [ int(n) for n in input_lines ]
    for idx in range(25, len(numbers)):
        if not is_XMAS_valid(numbers, idx):
            invalid_idx = idx
            yield(numbers[invalid_idx])
            break

    for idx in range(1, invalid_idx):
        for i in range(idx+1):
            this_set = [ n for n in numbers[i:idx] ]
            if sum(this_set) == numbers[invalid_idx]:
                yield(min(this_set) + max(this_set))
                return
    
    yield(None)

aoc.run(puzzles)
