#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def Check_Corrupted(line):

    left = {'(': ')', '[': ']', '{': '}', '<': '>'}
    right = {')': '(', ']': '[', '}': '{', '>': '<'}
    val = {')': 3, ']': 57, '}': 1197, '>': 25137}
    val2 = {')': 1, ']': 2, '}': 3, '>': 4}
    
    expected = []
    chars = list(line)
    if(chars[0] in right):
        # can't start with a closing bracket
        return val[chars[0]]
    for c in chars:
        if(c in left):
            expected.append(left[c]) # add the expected right closing bracket to the list
        else:
            ex = expected.pop()
            if(c != ex):  # this is not the expected closing bracket
                return val[c]
            # if it is expected, just continue since we've removed the partner

    return 0


def Fix_Line(line):

    left = {'(': ')', '[': ']', '{': '}', '<': '>'}
    right = {')': '(', ']': '[', '}': '{', '>': '<'}
    val = {')': 3, ']': 57, '}': 1197, '>': 25137}
    val2 = {')': 1, ']': 2, '}': 3, '>': 4}
    
    expected = []
    chars = list(line)
    if(chars[0] in right):
        # can't start with a closing bracket
        return -1
    for c in chars:
        if(c in left):
            expected.append(left[c]) # add the expected right closing bracket to the list
        else:
            ex = expected.pop()
            if(c != ex):  # this is not the expected closing bracket
                return -1
            # if it is expected, just continue since we've removed the partner

    # At this point (for part 2), we already have a list of expected characters.
    total = 0
    while(len(expected) > 0):
        ex = expected.pop()
        total *= 5
        total += val2[ex]

    return total


with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

#    total_corrupted = 0

    totals = []
    for line in lines:
#        val = Check_Corrupted(line)
#        total_corrupted += val
        res = Fix_Line(line)
        if(res != -1):
            totals.append(Fix_Line(line))
#    print("Corrupted",total_corrupted)

#print(totals)
s = sorted(totals)

print(s[ int(len(s)/2) ])  # middle item in list
