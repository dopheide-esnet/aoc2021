#!/usr/bin/env python3

testcase = False
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

def Calculate_Fuel(crabs,target):
    total = 0
    for c in crabs:
        diff = abs(target - c)
        total += diff * crabs[c]
    return total

def Calculate_Fuel2(crabs,target):
    total = 0

    for c in crabs:
        diff = abs(target - c)
        fuel_cost = 1
        for i in range(1,diff+1):
            total += fuel_cost * crabs[c]
            fuel_cost += 1

    return total

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    (min,max,crabs) = Input(lines[0])

#    print(min,max,crabs)

    ### for each position between and including min/max, calculate total fuel needed
    least_fuel = -1
    for target in range(min,max+1):
        res = Calculate_Fuel2(crabs,target)
        if(least_fuel == -1 or res < least_fuel):
            least_fuel = res
    print("Least Fuel:",least_fuel)
