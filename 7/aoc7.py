#!/usr/bin/env python3

testcase = True
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def Input(line):
    crabs = {}
    min = -1
    max = 0
    for num in line.split(','):
        n = int(num)
        if(min == -1 or n < min):
            min = n
        if(n > max):
            max = n
        if(n in crabs):
            crabs[n] += 1
        else:
            crabs[n] = 1
        
    return (min,max,crabs)

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    (min,max,crabs) = Input(lines[0])

    print(min,max,crabs)

