#!/usr/bin/env python3

testcase = True
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def Do_It(lines):
    return "Done"

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    print(bytes.fromhex(lines[0]))

#    res = Do_It(lines)
#    print("Result",res)



