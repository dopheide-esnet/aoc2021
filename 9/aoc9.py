#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def Build_Map(lines):
    map = []

    for line in lines:
        chars = list(line)
        digits = []
        for c in chars:
            digits.append(int(c))
        map.append(digits)
    return map

def Low_Spots(map):
    '''
    Find low spots, but we seemingly don't count low 'regions', like multiple 0's next to each other.
    '''
    total_risk = 0
    for y in range(len(map)):
        for x in range(len(map[y])):
            if(y==0 or (y > 0 and map[y][x] < map[y-1][x])):
                if(y == len(map)-1 or (y < len(map)-1 and map[y][x] < map[y+1][x])):
                    if(x==0 or (x > 0 and map[y][x] < map[y][x-1])):
                        if(x == len(map[y])-1 or (x < len(map[y])-1 and map[y][x] < map[y][x+1])):
                            total_risk += 1 + map[y][x]
    return total_risk

def Explore(map,basins,idx,y,x):
    '''
    y, x is the new location we're exploring from.
    '''
    if(y > 0 and (y-1,x) not in basins[idx] and map[y-1][x] != 9):
        # up
        basins[idx].append((y-1,x))
        Explore(map,basins,idx,y-1,x)
    if(x > 0 and (y,x-1) not in basins[idx] and map[y][x-1] != 9):
        # left
        basins[idx].append((y,x-1))
        Explore(map,basins,idx,y,x-1)
    if(y < len(map) - 1 and (y+1,x) not in basins[idx] and map[y+1][x] != 9):
        # down
        basins[idx].append((y+1,x))
        Explore(map,basins,idx,y+1,x)
    if(x < len(map[y]) - 1 and (y,x+1) not in basins[idx] and map[y][x+1] != 9):
        basins[idx].append((y,x+1))
        Explore(map,basins,idx,y,x+1)
    
#    print(basins)

def Basins(map):
    '''
    Find low spots (same as before) and expand them into basins.
    '''
    basins = {}
    for y in range(len(map)):
        for x in range(len(map[y])):
            if(y==0 or (y > 0 and map[y][x] < map[y-1][x])):
                if(y == len(map)-1 or (y < len(map)-1 and map[y][x] < map[y+1][x])):
                    if(x==0 or (x > 0 and map[y][x] < map[y][x-1])):
                        if(x == len(map[y])-1 or (x < len(map[y])-1 and map[y][x] < map[y][x+1])):

                            # Explore this basin
                            basins[(y,x)] = []
                            basins[(y,x)].append((y,x))
                            Explore(map,basins,(y,x),y,x)


    return basins


with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    map = Build_Map(lines)

    res = Low_Spots(map)

    print("Result:",res)

    basins = Basins(map)

    # crazy sort action
    s = dict(sorted(basins.items(), key=lambda item: len(item[1]), reverse=True))
    i = 0
    total = 1
    for b in s:
        total *= len(s[b])
        i += 1
        if i == 3:
            break

    print("Part2 Result:",total)


