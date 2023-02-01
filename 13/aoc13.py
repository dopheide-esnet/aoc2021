#!/usr/bin/env python3

import re

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def Build_Paper(lines):
    paper = []
    folds = []
    dots = []
    maxx = 0
    maxy = 0
    for line in lines:
        m = re.search(r'(\d+),(\d+)',line)
        if(m):
            x = int(m.group(1))
            y = int(m.group(2))
            dots.append((x,y))
            if(x > maxx):
                maxx = x
            if(y > maxy):
                maxy = y 
        else:
            n = re.search(r'fold along ([xy])=(\d+)',line)
            if(n):
                axis = n.group(1)
                num = int(n.group(2))
                folds.append((axis,num))
    for y in range(maxy+1):
        row = []
        for x in range(maxx+1):
            if((x,y) in dots):
                row.append("#")
            else:
                row.append(".")
        paper.append(row)
    return paper,folds

def fold_up(paper,num):
    for y in range(num+1,len(paper)):
        for x in range(len(paper[y])):
            newy = num - (y-num)
            if(paper[y][x] == '#'):
                paper[newy][x] = "#"
    # after the folding is complete, trim the bottom of the paper off
    paper = paper[0:num]            
    return paper

def fold_left(paper,num):
    print("Folding Left")
    for y in range(len(paper)):
        for x in range(num+1,len(paper[y])):
            newx = num - (x-num)
            if(paper[y][x] == '#'):
                paper[y][newx] = '#'
        paper[y] = paper[y][0:num]

    return paper

def print_paper(paper):
    for y in range(len(paper)):
        for x in range(len(paper[y])):
            print(paper[y][x],end='')
        print()

def count_dots(paper):
    total = 0
    for y in range(len(paper)):
        for x in range(len(paper[y])):
            if(paper[y][x] == '#'):
                total += 1
    return total

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    paper, folds = Build_Paper(lines)

    # Part 1, just do first fold
    (axis,num) = folds.pop(0)
    if(axis == 'y'):
        paper = fold_up(paper,num)
    else:
        paper = fold_left(paper,num)

    # testing Fold_left with Part 1
#    (axis,num) = folds.pop(0)
#    paper = fold_left(paper,num)

    res = count_dots(paper)
    print("Part1:",res)

    for fold in folds:
        (axis,num) = fold
        if(axis == 'y'):
            paper = fold_up(paper,num)
        else:
            paper = fold_left(paper,num)
    
    print_paper(paper)







