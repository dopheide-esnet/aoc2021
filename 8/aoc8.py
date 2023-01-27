#!/usr/bin/env python3

'''
A lot of this didn't feel very efficient, but the input isn't that large.
'''

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def Count_Easy_Digits(lines):
    total = 0
    for line in lines:
        input = line.split(" | ")
        digits = input[1].split(" ")
        for d in digits:
            l = len(d)
            if(l == 2 or l == 4 or l == 3 or l ==7):
                total += 1
    return total

#  aaaa
# b    c
# b    c
#  dddd
# e    f
# e    f
#  gggg 


def Determine_Digits(lines):
    rtotal = 0
    for line in lines:
        segments = {}
        input = line.split(" | ")
        digits = input[0].split(" ")
        one = []
        two = []
        three = []
        four = []
        five = []
        seven = []
        test = []

        # will need to re-process until we're done.
        while(len(segments) < 7):
            for d in digits:
                l = len(d)
                if(l == 2):    #or l == 4 or l == 3 or l ==7):
                    # number 1
                    one = list(d) # these two characters are in the place of c or f
                elif(len(one) > 0 and l == 3):
                    # number 7
                    # we know the character not part of 'one' is on top.
                    seven = list(d)
                    for c in seven:
                        if c not in one:
                            segments['a'] = c
                elif(len(one) > 0 and l == 5):
                    # if we have 'one', we know that a 5 segment number with both of those characters is 'three'
                    test = list(d)
                    if(one[0] in d and one[1] in d):
                        three = test

                    # okay, so if we have three and 'b', 'five' will help us define f. with f and one, we have c
                    elif len(three) > 0 and 'b' in segments and segments['b'] in test and len(five)==0:
                        # this is 'five'
                        five = test
                        for c in one:
                            if c in five:
                                segments['f'] = c
                        for c in one:
                            if c != segments['f']:
                                segments['c'] = c
                    
                    elif len(three) > 0 and 'c' in segments and segments['f'] not in test and len(two)==0:
                        # so this could be three also as it sits.
                        two = test
                        for c in two:
                            if c not in one and c not in five:
                                segments['e'] = c

                elif(len(three) > 0 and l == 4):
                    # with three, we can determine 'b' from number 'four'
                    four = list(d)
                    for c in four:
                        if c not in three:
                            segments['b'] = c
                    # also.. we have 'b' and 'one', so we know from 'four' what 'd' is.
                    for c in four:
                        if c not in one and c != segments['b']:
                            segments['d'] = c
                    # conveniently, with segement 'a' also, we can determine 'g' using 'three'
                    for c in three:
                        if c not in four and 'a' in segments and c != segments['a']:
                            segments['g'] = c
#                print(segments)

        # finish defining the other numbers
        rzero = ['a','b','c','e','f','g']
        zero = []
        for c in rzero:
            zero.append(segments[c])
#        rtwo = ['a','c','d','e','g']
#        two = []
#        for c in rtwo:
#            two.append(segments[c])
        rsix = ['a','b','d','e','f','g']
        six = []
        for c in rsix:
            six.append(segments[c])
        # eight's just based on size alone
        rnine = ['a','b','c','d','f','g']
        nine = []
        for c in rnine:
            nine.append(segments[c])

#        print("Known:",segments)

        results = input[1].split(" ")

        num = ""
        for r in results:
            
            if(len(r) == 2):
                num += "1"
            elif(len(r) == 4):
                num += "4"
            elif(len(r) == 3):
                num += "7"
            elif(len(r) == 7):
                num += "8"
            elif(len(r) == 5):
                # 2, 3, or 5
                is_two = True
                is_three = True
                for c in list(r):
                    if c not in two:
                        is_two = False
                    if c not in three:
                        is_three = False
                if(is_two):
                    num += "2"
                elif(is_three):
                    num += "3"
                else:
                    num += "5"
            elif(len(r) == 6):
                # 0, 6 or 9
                is_zero = True
                is_six = True
                for c in list(r):
                    if c not in zero:
                        is_zero = False
                    if c not in six:
                        is_six = False
                if(is_zero):
                    num += "0"
                elif(is_six):
                    num += "6"
                else:
                    num += "9"

        rtotal += int(num)


    return rtotal


with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    res = Determine_Digits(lines)

    print("Result",res)



