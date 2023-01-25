#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def Dive(lines):
    x = 0
    y = 0

    for line in lines:
        (d, val) = line.split(" ")
        num = int(val)

        if(d == 'forward'):
            x += num
        elif(d == 'down'):
            y += num
        elif(d == 'up'):
            y -= num
    return x*y

def Aim(lines):
    x = 0
    y = 0
    aim = 0

    for line in lines:
        (d, val) = line.split(" ")
        num = int(val)

        if(d == 'forward'):
            x += num
            y += num * aim
        elif(d == 'down'):
            aim += num
        elif(d == 'up'):
            aim -= num

    return x*y

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    res = Dive(lines)
    print("Result",res)

    res = Aim(lines)
    print("With Aim:", res)



