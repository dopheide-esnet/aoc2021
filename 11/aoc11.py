#!/usr/bin/env python3

import time

class Octopus:
    def __init__(self, val):
        self.val = val
        self.flashed = False

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def gen_map(lines):
    '''
    From input, generate our octomap
    '''
    map = []
    for line in lines:
        nums = list(line)
        row = []
        for d in nums:
            row.append(Octopus(int(d)))
        map.append(row)
    return map

def print_map(map):
    '''
    Print the current octomap state
    '''
    for y in range(len(map)):
        for x in range(len(map[y])):
            val = map[y][x].val
            if(val == 0):
                print("\033[1m%d\033[0m" % val,end='')
            else:
                print(val,end='')
        print()


def Update(map,y,x):
    if(map[y][x].flashed == False):
        map[y][x].val += 1
        if(map[y][x].val > 9):
            return True
    return False

def Run_Steps(map,steps):
    '''
    Run through the number of required steps for the octopi.
    '''
    flashes = 0
    for s in range(steps):
        synced = 0
        nines = []
        # Increase all values by 1, keep track of 9's and set them all back to not flashed.
        for y in range(len(map)):
            for x in range(len(map[y])):
                if(map[y][x].val == 10):
                    print("oops")
                    exit()
                map[y][x].val += 1
                map[y][x].flashed = False
                if(map[y][x].val > 9):
                    nines.append((y,x))
        
#        print_map(map)
#        print()
#        print("nines",nines)

        # Process the 9s and add surrounding new nines to the list.
        # Actually the numbers > 9
        f = 0
        while(len(nines) > 0):
            new_nines = []
            for n in nines:
                (y,x) = n
                map[y][x].val = 0
                flashes += 1
                synced += 1
                map[y][x].flashed = True

                # check all eight adjacent squares
                if(y>0):
                    if(x>0):
                        if(Update(map,y-1,x-1) and (y-1,x-1) not in nines):
                                new_nines.append((y-1,x-1))
                    if(Update(map,y-1,x) and (y-1,x) not in nines):
                            new_nines.append((y-1,x))
                    if(x < len(map[y]) - 1):
                        if(Update(map,y-1,x+1) and (y-1,x+1) not in nines):
                            new_nines.append((y-1,x+1))
                if(y < len(map)-1):
                    if(x>0):
                        if(Update(map,y+1,x-1) and (y+1,x-1) not in nines):
                            new_nines.append((y+1,x-1))
                    if(Update(map,y+1,x) and (y+1,x) not in nines):
                        new_nines.append((y+1,x))
                    if(x < len(map[y]) - 1):
                        if(Update(map,y+1,x+1) and (y+1,x+1) not in nines):
                            new_nines.append((y+1,x+1))                
                if(x>0):
                    if(Update(map,y,x-1)and (y,x-1) not in nines):
                        new_nines.append((y,x-1))
    # skip self
    #            if(Update(map,y,x)):
    #                nines.append((y,x))
                if(x < len(map[y]) - 1):
                    if(Update(map,y,x+1) and (y,x+1) not in nines):
                        new_nines.append((y,x+1))
            nines = set(new_nines)  # Make it a set to remove duplicates!  Very important!
            f+=1
#            if(s == 1 and (f==2 or f==3 )):
#                print("new:",new_nines)
#                print_map(map)
#                if(f==3):
#                    exit()

        # Pretty to watch it sync...
        print_map(map)
        print()
        time.sleep(0.1)

        if(synced == len(map) * len(map[0])):
            print("Synchronized at step:",s+1)
            exit()
    return flashes


with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    octomap = gen_map(lines)
#    print_map(octomap)

    steps = 400  # set sufficiently high to catch the synchronized state
    flashes = Run_Steps(octomap,steps)

#   Run_Steps modified for Part 2
    print_map(octomap)
    print("Flashes:",flashes)




