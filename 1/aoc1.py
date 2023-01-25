#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def Count_Increased(lines):

    current = int(lines[0])
    increased = 0
    for i in range(1,len(lines)):
        next = int(lines[i])
        if(next > current):
            increased += 1
        current = next
    return increased

def Count_Increased_Sliding(lines):

    current = int(lines[0]) + int(lines[1]) + int(lines[2])
    increased = 0
    for i in range(1,len(lines)-2):  # stop when there's not enough for the next window
        next = int(lines[i]) + int(lines[i+1]) + int(lines[i+2])
        if(next > current):
            increased += 1
        current = next
    return increased     

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    res = Count_Increased(lines)
    print("Increased",res)

    res = Count_Increased_Sliding(lines)
    print("Sliding:",res)

