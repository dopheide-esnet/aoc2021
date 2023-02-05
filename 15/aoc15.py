#!/usr/bin/env python3

import copy

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

class Path:
    def __init__(self):
        self.total = 0
        self.path = []

def Build_Map(lines):
    map = []
    for line in lines:
        row = []
        for d in list(line):
            row.append(int(d))
        map.append(row)
    return map

def print_map(map):
    for y in range(len(map)):
        for x in range(len(map[y])):
            print(map[y][x],end='')
        print()

def Find_Path(map,paths,shortest,cur_path,y,x,cost):
    ''' Oh right, do depth first '''
    cost += map[y][x]
    if((y,x) not in shortest):
        shortest[(y,x)] = cost # The lowest cost path to get to this coordinate
    elif(cost < shortest[(y,x)]):
        shortest[(y,x)] = cost
    else:
        return # got here cheaper before, stop

    c_path = copy.copy(cur_path)
    c_path.append((y,x))
    
    # As soon as we have A path to the end, end any path that has a count higher than that.
    # Can eliminate more if they're 'too far' to get there.

    if(len(paths) > 0):
        for p in paths:
            (pcost,cp) = p
            if(cost >= pcost):
                return


    if((y,x) == (len(map)-1,len(map[y])-1)):
        # end of this potential path.
        paths.append((cost,c_path))
        return   # at the end, stop
        
    if(y < len(map) - 1):
        Find_Path(map,paths,shortest,c_path,y+1,x,cost)
    if(x < len(map[y])-1):
        Find_Path(map,paths,shortest,c_path,y,x+1,cost)
    if(y > 0):
        Find_Path(map,paths,shortest,c_path,y-1,x,cost)
    if(x > 0):
        Find_Path(map,paths,shortest,c_path,y,x-1,cost)

def Expand_Map(map):
    big_map = []
    for big_y in range(5):
        for y in range(len(map)):
            row = []
            for big_x in range(5):
                for x in range(len(map[y])):
                    by = y + len(map) * big_y
                    bx = x + len(map[y]) * big_x

                    val = map[y][x] + 1 * big_y + 1 * big_x
                    if (val > 9):
                        val -= 9
                    row.append(val)
            big_map.append(row)

    return big_map

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    map = Build_Map(lines)

    #print_map(map)
    paths = []
    shortest = {(0,0): 0}
    cur_path = []
    Find_Path(map,paths,shortest,cur_path,1,0,0)
    Find_Path(map,paths,shortest,cur_path,0,1,0)
#    print(shortest)
#    print(paths)

    if((len(map)-1,len(map[0])-1) in shortest):
        print(shortest[(len(map)-1,len(map[0])-1)])
    else:
        print("Error, never found the end")
    
    # Part 2.  Maybe just expanding the map and doing the same is naive, but
    # we'll give it a shot.

    big_map = Expand_Map(map)
    # print_map(big_map)
    paths = []
    shortest = {(0,0): 0}
    cur_path = []
    Find_Path(big_map,paths,shortest,cur_path,1,0,0)
    Find_Path(big_map,paths,shortest,cur_path,0,1,0)

    if((len(big_map)-1,len(big_map[0])-1) in shortest):
        print(shortest[(len(big_map)-1,len(big_map[0])-1)])
    else:
        print("Error, never found the end")    
    
