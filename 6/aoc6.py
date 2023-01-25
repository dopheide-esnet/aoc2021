#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def Initialize_Fish(input):
    ''' Fish only have nine possible states, 0-8 '''

    fish = {}
    for i in range(9):
        fish[i] = 0

    for fishy in input.split(','):
        if(int(fishy) in fish):
            fish[int(fishy)] += 1
        else:
            print("Error, bad fish")
            exit()

    return fish

def Count_Fish(fish):
    total = 0
    for i in range(len(fish)):
        total += fish[i]
    
    return total

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    fish = Initialize_Fish(lines[0])

    days = 256
    day = 0
    while(day < days):
        old = 0
        for i in range(9):
            if(i==0):
                old = fish[i]
            if(i < 8):
                fish[i] = fish[i+1]
            if(i == 6):
                fish[i] += old
        fish[8] = old # all the old fish make new fish
        day += 1

    res = Count_Fish(fish)
    print("Result:",res)

    # track fish by how many days they have in a dict.
    # ie   {1: 6} would be 6 fish with a timer of 1.  It should be much easier to scale this way.



