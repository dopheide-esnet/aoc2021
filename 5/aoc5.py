#!/usr/bin/env python3

import re

class Map:
    def __init__(self, m, maxx, maxy):
        self.map = m
        self.mx = maxx
        self.my = maxy
    def print(self):
        for y in range(maxy+1):
            for x in range(maxx+1):
                print(self.map[(x,y)],end='')
            print()
    def answer(self):
        total = 0
        for y in range(maxy+1):
            for x in range(maxx+1):
                if(self.map[(x,y)] != '.'):
                    if(self.map[(x,y)] > 1):
                        total += 1
        return total

def Get_Vents(lines):
    vents = []
    for line in lines:
        m = re.search(r'(\d+),(\d+) \-\> (\d+),(\d+)',line)
        if(m):
            vents.append({'x1': int(m.group(1)),
                      'y1': int(m.group(2)),
                      'x2': int(m.group(3)),
                      'y2': int(m.group(4))})
    return vents

def Extents(vents):
    x = 0
    y = 0
    for v in vents:
        if(v['x1'] > x):
            x = v['x1']
        if(v['x2'] > x):
            x = v['x2']
        if(v['y1'] > y):
            y = v['y1']
        if(v['y2'] > y):
            y = v['y2']
    return (x,y)

def Build_Map(vents,maxx,maxy):
    map = {}
    # populate blank map
    for y in range(maxy+1):
        for x in range(maxx+1):
            map[(x,y)] = '.'

    # Process the straight-line vents only for Part 1
    for v in vents:
        if(v['x1'] == v['x2']):
            if(v['y1'] < v['y2']):
                y = v['y1']
                my = v['y2']
            else:
                y = v['y2']
                my = v['y1']
            for i in range(y,(my+1)):
                if(map[(v['x1'],i)] == '.'):
                    map[(v['x1'],i)] = 1
                else:
                    map[(v['x1'],i)] += 1
        elif(v['y1'] == v['y2']):
            if(v['x1'] < v['x2']):
                x = v['x1']
                mx = v['x2']
            else:
                x = v['x2']
                mx = v['x1']
            for i in range(x,(mx+1)):
                if(map[(i,v['y1'])] == '.'):
                    map[(i,v['y1'])] = 1
                else:
                    map[(i,v['y1'])] += 1

        else:
            # In part 2, we also handle the diagonals
            r = 0
            if(v['x1'] < v['x2']):
                x = v['x1']
                mx = v['x2']
                if(v['y1'] < v['y2']):
                    y = v['y1']
                    my = v['y2']
                else:
                    y = v['y2']
                    my = v['y1']
                    r = 1
            else:
                x = v['x2']
                mx = v['x1']
                if(v['y1'] < v['y2']):
                    y = v['y1']
                    my = v['y2']
                    r = 1
                else:
                    y = v['y2']
                    my = v['y1']

            # r indicates if we need to reverse the y range.
            if(r == 0):
                j = 0
                for i in range(x,(mx+1)):
                    if(map[(i,y+j)] == '.'):
                        map[(i,y+j)] = 1
                    else:
                        map[(i,y+j)] += 1
                    j+=1
            else:
                j = 0
                for i in range(x,(mx+1)):
                    if(map[(i,my-j)] == '.'):
                        map[(i,my-j)] = 1
                    else:
                        map[(i,my-j)] += 1
                    j+=1

    m = Map(map,maxx,maxy)
    return m

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    vents = Get_Vents(lines)
    (maxx, maxy) = Extents(vents)
#    print("max:",maxx,maxy)
    map = Build_Map(vents,maxx,maxy)
#    map.print()

    print("Result",map.answer())





