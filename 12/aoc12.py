#!/usr/bin/env python3

import re

class Cave:
    def __init__(self,name,size):
        self.name = name
        self.size = size
        self.neighbors = []        

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def parse_caves(lines):
    caves = {}
    for line in lines:
        (a,b) = line.split('-')
        # making start and end uppercase makes the path finding easier.
        if(a == 'start'):
            a = "START"
        elif(a == 'end'):
            a = "END"
        if(b == 'end'):
            b = "END"
        elif(b == 'start'):
            b = "START"
        for c in (a,b):
            size = "small"   # default
            if(c not in caves):
                if(c.isupper() and c!='END' and c!='START'):
                    size = "big"
                caves[c] = Cave(c,size)
        caves[a].neighbors.append(b)
        caves[b].neighbors.append(a)
    return caves

def cave_paths(caves,paths,loc,cur_path):

    for n in caves[loc].neighbors:
        if((n.islower() and n in cur_path) or (n=='START')): # this is why we make START and END uppercase
            continue
        elif(n == 'END'):
            new_path = cur_path + n
            if(new_path not in paths):
                paths.append(new_path)
        else:
            new_path = cur_path + n
            cave_paths(caves,paths,n,new_path)
    return

def cave_paths_2(caves,paths,loc,c_path):
    '''
    Part 2, one of the small caves can be visited twice.
    For this we'll make a cur_path a dict.
    '''
    c = list(c_path.keys())
    cur_path = c[0]
    s_cave = c_path[cur_path]
    for n in caves[loc].neighbors:
        if((n.islower() and n in cur_path and s_cave != '') or (n=='START')): # this is why we make START and END uppercase
            continue
        elif(n == 'END'):
            new_path = cur_path + n
            if(new_path not in paths):
                paths.append(new_path) # be sure to pick up the small cave value.
        else:
            if(n.islower() and n in cur_path):
                s_cave = n
                new_path = cur_path + n
                cave_paths_2(caves,paths,n,{new_path: s_cave})
                s_cave = '' # set this back to blank for the rest of the loop
            else:
                new_path = cur_path + n
                cave_paths_2(caves,paths,n,{new_path: s_cave})
            
    return


with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    caves = parse_caves(lines)

    pc = False
    if(pc):
        for c in caves:
            print("%s: " % c, end='')
            for n in caves[c].neighbors:
                print("%s " % n, end='')
            print()

    paths = []
    cave_paths(caves,paths,"START","START")

#    print(paths)
    print("Number of paths:",len(paths))

    paths = []
    cave_paths_2(caves,paths,"START",{"START": ""})

    print("Number of paths:",len(paths))

    pp = False
    if(pp):
        for p in paths:
            m = re.search(r'START(\w+)END',p)
            if(m):
                caves = list(m.group(1))
            print("start,",end='')
            for c in caves:
                print(f"{c},",end='')
            print("end")

# maybe track paths as just a string?

# never revisit start, but that's fine cause it's 'small'
