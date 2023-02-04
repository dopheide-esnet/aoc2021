#!/usr/bin/env python3

import re
import copy

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def get_input(lines):
    polymer = list(lines.pop(0))
    lines.pop(0)
    rules = {}
    for line in lines:
        (pair,ins) = line.split(" -> ")
        rules[pair] = ins
    return (polymer,rules)

def build_poly(polymer,rules):
    needed = {}
    p = "".join(polymer)
#    for r in rules:
    # Is regex going to be too slow for this?
    # It also doesn't work for instance, BBB only matches once for BB.
#        idxs = [m.start() for m in re.finditer(r, p)]

    for i in range(len(polymer)-1):
        p = polymer[i]+polymer[i+1]
        if p in rules:
            needed[i] = rules[p]

#        for i in idxs:
#            needed[i] = rules[r]
    needed = dict(sorted(needed.items()))

#    print("Needed:",needed)

    i = 0
    for n in needed:

        # works unless we skip an index... but that shouldn't be an issue.
#        print("n-i:",n-i)

        # each time we add a character the polymer is longer and we need to add 'i' to where it goes
#        if((n-i) == 0):
        polymer.insert(n+i+1,needed[n])
        i += 1

def Do_Pairs(polymer,rules,cur_depth,target_depth):
    '''
    Instead of inserting for every single pair, we count up the number of each
    unique pair, see that that polymer looks like and count those.  Do that a couple
    times recursively and it should be much faster.
    '''

    # How can we improve this?
    # Can we save what the count for depth 4 or whatever looks like for a given pair
    #   and just add that?  Add not just the count, but the number of each new pairs created?

    pairs = {}
    for i in range(len(polymer)-1):
        p = polymer[i] + polymer[i+1]
        if p in pairs:
            pairs[p] += 1
        else:
            pairs[p] = 1

    counts = {}
    for p in pairs:
        new_poly = list(p)
        if(target_depth - cur_depth > 4):
            for i in range(4):
                build_poly(new_poly,rules)
            new_depth = 4
        else:
            for i in range(target_depth-cur_depth):
                build_poly(new_poly,rules)
            new_depth = target_depth - cur_depth
        # how do we count the letters given this?
        # Be careful not to count the the overlapping characters from the pairs twice.

        last_pair = "".join(polymer[-2:])

        if(p != last_pair):
            # count all but last character times how many of those pairs
            if cur_depth + new_depth == target_depth:
                nc = count_parts(new_poly[:-1])
            else:
                nc = Do_Pairs(new_poly,rules,cur_depth+new_depth,target_depth)

                if(new_poly[len(new_poly)-1] in nc):
                    nc[new_poly[len(new_poly)-1]] -= 1 # don't double count the connector
                else:
                    print("Error: Shouldn't be true")
                    exit()
        else:

            # todo:  if it is the last pair, we need to only count the extra once
            minus_last_char = new_poly[len(new_poly)-1]
            mlc_num = pairs[p] - 1

            if cur_depth + new_depth == target_depth:
                nc = count_parts(new_poly)
            else:
                nc = Do_Pairs(new_poly,rules,cur_depth + new_depth,target_depth)
            # count all characters times how many of those pairs
        # Add nc into counts
        # todo, can't just multiply because the last
        # pair is counted differently.
        for c in nc:
            if c in counts:
                counts[c] += nc[c] * pairs[p]
            else:
                counts[c] = nc[c] * pairs[p]

    # TODO:  But maybe only do the subtraction if we're at full depth?
    counts[minus_last_char] -= mlc_num

    return(counts)


def build_poly_2(polymer,rules,target_depth):
    cur_depth = 0

    # build up a little to start with
    if(target_depth > 12):
        cur_depth += 12
        for i in range(12):
            build_poly(polymer,rules)
    else:
        print("You don't need me")
        exit()

    counts = Do_Pairs(polymer,rules,cur_depth,target_depth)
    return counts

def count_parts(polymer):
    counts = {}
    for p in polymer:
        if p in counts:
            counts[p] += 1
        else:
            counts[p] = 1
    return counts

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()
    copy_lines = copy.copy(lines)  # keep this for Part 2
    (polymer,rules) = get_input(lines)
    
#    print(polymer)
#    print(rules)

    for i in range(10):
        build_poly(polymer,rules)

#    print(polymer)
    counts = count_parts(polymer)
#    print(counts)
    min = -1
    max = 0
    for c in counts:
        if(min == -1 or counts[c] < min):
            min = counts[c]
        if(counts[c] > max):
            max = counts[c]
    print("Result:",max-min)
#    print("".join(polymer))

# Part 2 thoughts... oh shit.
# I think I can break up the polymer into repeatable strands.

# or.. let's say at every 5 steps, we split each two char pair into it's own polymer string copy and keep
# track of how many of those there are.

    # start fresh for part two
    (polymer,rules) = get_input(copy_lines)

    counts = build_poly_2(polymer,rules,40)

    min = -1
    max = 0
    for c in counts:
        if(min == -1 or counts[c] < min):
            min = counts[c]
        if(counts[c] > max):
            max = counts[c]
    print("Result:",max-min)

    print("remember, doing input2.txt right now")
    ## seems like if we start with just one pair, it doesn't take long.
    #  could just break up the initial input again and combine counts
    #  but , it finished with pypy3 in 34min and I'm tired of this one.




