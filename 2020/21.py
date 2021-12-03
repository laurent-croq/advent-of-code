#!/usr/bin/python3

import os,sys
sys.path.append(os.path.normpath(sys.argv[0]+"/../.."))

import aoc

import itertools,re

def find_allergens(foods, ing2all = {}):
    if len(foods) == 0:
        return(ing2all)

    remaining_alls = list(set(foods[0]['allergens'])-set(ing2all))
    remaining_ings = list(set(foods[0]['ingredients'])-set(ing2all.values()))

    for candidate_ings in itertools.combinations(range(len(remaining_ings)), len(remaining_alls)):
        for ing_map in itertools.permutations(candidate_ings):
            new_ing2all = ing2all.copy()

            for ingredient, allergen in zip([ remaining_ings[i] for i in ing_map ], remaining_alls):
                new_ing2all[allergen] = ingredient
                if ing2all.get(allergen, None) not in (None, ingredient):
                    continue

                for f in foods[1:]:
                    if allergen in f['allergens'] and ingredient not in f['ingredients']:
                        break
                else:
                    continue
                break
            else:
                res = find_allergens(foods[1:], new_ing2all)
                if res is not None:
                    return(res)

def puzzles(input_lines, **extra_args):
    foods = []

    for line in input_lines:
        m = re.match(r'(.*) \(contains (.*)\)', line)
        foods.append({ "ingredients": m.group(1).split(" "), "allergens": m.group(2).split(", ") })

    ingredients_with_allergens = find_allergens(foods)

    yield(sum(len(set(f['ingredients']).difference(ingredients_with_allergens.values())) for f in foods))
    yield(",".join([ v[1] for v in sorted(ingredients_with_allergens.items(), key=lambda v: v[0]) ] ))

aoc.run(puzzles)
