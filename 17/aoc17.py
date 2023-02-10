#!/usr/bin/env python3

import re

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def Input(line):
    ''' target = [xmin, xmax, ymin, ymax] '''
    # target area: x=20..30, y=-10..-5
    m = re.search(r'x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)',line)
    if(m):
        target = []
        target.append(int(m.group(1)))
        target.append(int(m.group(2)))
        target.append(int(m.group(3)))
        target.append(int(m.group(4)))
    else:
        print("Error, regex failed")
        exit()
    return target

def Find_Minimum_X(xmin,xmax):
    ''' 
    Find initial x velocities that result in vx=0 withing the target range.
    Vx's bigger than that won't be useful for finding the highest Vy.
    '''
    i = 1  # starting x velocity
    useful_x = []
    while(1):
        x = 0
        vx = i
        steps = 1
        while(vx > 0):
            x += vx
            if(x >= xmin and x <= xmax):
                useful_x.append(i)
#                return (i,steps)
            elif(x > xmax):
                return set(useful_x)
            vx -= 1
            steps += 1
        i+=1

def Find_Y(target,vx,initial_y):

    xmin = target[0]
    xmax = target[1]
    ymax = target[3]
    ymin = target[2]

    vymax = 0
    steps = 1
    x = 0
    y = 0

    vy = initial_y
    while(y > ymin):  # while y is above ymin...
        x += vx
        y += vy
#        print("x,y",x,y)

# this is dumb, of course vy will be zero at the apex.
#        if(vy == 0 and y > ymin):
#            print("here1")
#            return vymax
        if(y <= ymax and y >= ymin):
            if(initial_y >= vymax and x >= xmin and x <= xmax):
                vymax = initial_y
            elif(y < ymin):
                return vymax  # TODO, make a separate function so we can return
        vy -= 1
        if(vx > 0):
            vx -= 1
        steps += 1

    return vymax

def Shoot(target):
    '''
    Try different x and y velocities.  We know our test shots don't work if they
    get past xmax or ymin without hitting the target.
    '''
    start = (0,0)
    vxs = Find_Minimum_X(target[0],target[1])
    ymax = target[3]
    ymin = target[2]

    # we don't want a big vx at all when looking for a high vy.
    # I think we allow any initial vx where vx ends up being 0 within the x range.
#    print(vxs)

    # okay.. since we start at 0,0 if our vy is bigger than y=0 to y=ymin, by
    # the time it's on it's way down it'll never hit the target area.
    vy_bound = abs(ymin)

    vymax = 0
    for vx in vxs:
        i = 1  # starting y velocity
        while(1):
            x = 0
            y = 0
            vy = i

            if(vy > vy_bound):
                break

            new_vymax = Find_Y(target,vx,vy)
            if(new_vymax > vymax):
                vymax = new_vymax
            i+=1

    return vymax

def Find_Y2(target,vx,initial_y,on_target):

    xmin = target[0]
    xmax = target[1]
    ymax = target[3]
    ymin = target[2]

    steps = 1
    x = 0
    y = 0

    initial_vx = vx
    vy = initial_y
    while(y > ymin):  # while y is above ymin...
        x += vx
        y += vy

        if(y <= ymax and y >= ymin):
            if(x >= xmin and x <= xmax):
                ## On Target!
                if((initial_vx,initial_y) not in on_target):
                    on_target.append((initial_vx,initial_y))
            elif(y < ymin):
                return
        vy -= 1
        if(vx > 0):
            vx -= 1
        steps += 1

    return


def Shoot2(target,on_target):

    start = (0,0)
    vxs = Find_Minimum_X(target[0],target[1])
    ymax = target[3]
    ymin = target[2]

    # For Part 2
    vxmax = target[1]+1
    vymin = target[2]-1
    
    vy_bound = abs(ymin)

    print("min,max",min(vxs),vxmax+1)
    for vx in range(min(vxs),vxmax+1):

        # TODO, can do negative initial y velocities.


        i = vymin  # starting y velocity
        while(1):
            vy = i

            if(vy > vy_bound):
                break

            Find_Y2(target,vx,vy,on_target)
            i+=1

    return

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    target = Input(lines[0])
    print("Result",target)

    vymax = Shoot(target)

    # What was the max y seen?
    maxy = 0
    y = 0
    vy = vymax
    while(vy > 0):
        y += vy
        vy -= 1
    print("Result:",y)

    # Part 2... so now's when we get to vxmax a vx that goes past the target area
    # on the first shot.
    # start at the min of vxs, go to vxmax.  Save any vy that ends up in the target

    # Copy and modify functions for Part 2

    on_target=[]
    Shoot2(target,on_target)
    for t in on_target:
        (x,y) = t
#        print("%s,%s" % (x,y))


    print(len(set(on_target)))





