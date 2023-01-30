#!/usr/bin/env python3

import re

class Cave:
    def __init__(self,name,size):
        self.name = name
        self.size = size
        self.neighbors = []        

testcase = True
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def parse_caves(lines):
    caves = {}
    for line in lines:
        (a,b) = line.split('-')
        for c in (a,b):
            size = "small"   # default
            if(c not in caves):
                if(re.match(r'[A-Z]+',c)):
                    size = "big"
                caves[c] = Cave(c,size)
        caves[a].neighbors.append(b)
        caves[b].neighbors.append(a)
    return caves

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    caves = parse_caves(lines)

    pc = True
    if(pc):
        for c in caves:
            print("%s: " % c, end='')
            for n in caves[c].neighbors:
                print("%s " % n, end='')
            print()

    print("now find paths")

# maybe track paths as just a string?

# never revisit start, but that's fine cause it's 'small'
