#!/usr/bin/env python3

import math
import copy

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

class Number:
    def __init__(self,parent,lval,rval):
        self.parent = parent
        self.lval = lval
        self.rval = rval
        self.left = None
        self.right = None
    def print_vals(self):
        print("parent:",self.parent)
        print("lval:",self.lval)
        print("rval:",self.rval)
        print("left:",self.left)
        print("right:",self.right)
   
    def p_recurse(self,num):
        number = [',']
        if(num.rval == None):
            r_num = self.p_recurse(num.right)
            number.extend(r_num)
        else:
            number.append(str(num.rval))
        number.append(']')

        if(num.lval == None):
            l_num = self.p_recurse(num.left)
            # prepend
            number = l_num + number
        #    number.extend(r_num)
        else:
            number.insert(0,str(num.lval))
        number.insert(0,'[')
        return number

    def print(self):
        number = self.p_recurse(self)
        print("".join(number))
    
    def return_print(self):
        number = self.p_recurse(self)
        return "".join(number)

        
def Max_Depth(line):
    '''
    If max_depth > 4 then this number needs reduced.
    '''
    md = 0
    depth = 0
    for c in line:
        if(c == '['):
            depth += 1
        elif(c == ']'):
            depth -= 1
        if(depth > md):
            md = depth
    return md

def Middle_Index(line):
    depth = 0
    for i in range(len(line)):
        if(line[i] == '['):
            depth += 1
        elif(line[i] == ']'):
            depth -= 1
        if(line[i] == ',' and depth == 1):
            return i

def Process_Number(parent_num,line):
    # cur_num is the parent is most cases.
    middle = Middle_Index(line)

    # so we build a Number.
    # everything to the left minus a '[' can go back through this.
    # everything to the right, likewise.

    lval = None
    rval = None
    if(line[middle-1].isdigit()):
        lval = int(line[middle-1])
    if(line[middle+1].isdigit()):
        rval = int(line[middle+1])

    if(parent_num == None):
        cur_num = Number(None,lval,rval)
    else:
        cur_num = Number(parent_num,lval,rval)

    if(lval != None and rval != None):
        # both were digits, return
        return cur_num

    if lval == None:
        left = line[1:middle]
        left_num = Process_Number(cur_num,left)
        cur_num.left = left_num

    if rval == None:
        right = line[middle+1:]
        right_num = Process_Number(cur_num,right)
        cur_num.right = right_num

    return cur_num

def Read_Numbers(lines):
    '''
    Let's try a different way, try to find the 'top' pair.
    The 'middle' comma as it were.  Then read left and right from there.
    '''
    numbers = []  # list of all numbers in our input
    for line in lines:
        num = Process_Number(None,line)
        numbers.append(num)
    return numbers

def Add_Numbers(one,two):
    new_num = Number(None,None,None)
    one.parent = new_num
    two.parent = new_num
    new_num.left = one
    new_num.right = two

    return new_num

def Find_Left_Pair(number,depth):
        '''
        Returns result_number and a bool for whether it was the left branch or right branch
        '''
#        print("Finding left for:")
#        number.print()
        # could we do this differently?  The depth only matters as a test to see if we've found the right
        # bottom pair (as defined by not having a .left or .right)

        if(depth == 5 and number.left == None and number.right == None):
            return (number,None)  # yay!
#        elif(number.left == None and number.right == None):
#            print("go back")
#            return None

        depth += 1
        if(number.left != None):  
            (res_num,is_left) = Find_Left_Pair(number.left,depth)
            if(res_num != None):
                if(is_left != None):
                    return (res_num,is_left)
                else:
                    return (res_num,True)
#            else:
#                return None
        if(number.right != None):
            (res_num,is_left) = Find_Left_Pair(number.right,depth)
            if(res_num != None):
                if(is_left != None):
                    return (res_num,is_left)
                else:
                    return (res_num,False)
            else:
                return (None,None)            

#        exit()
        return (None,None)

def Find_Left_Split(number):
        
#        print("Finding left for:")
#        number.print()
        # could we do this differently?  The depth only matters as a test to see if we've found the right
        # bottom pair (as defined by not having a .left or .right)

        if(number.left != None):
            rnumber = Find_Left_Split(number.left)
            if(rnumber != None):
                number.left = rnumber
                return number
        elif(number.lval > 9):
#            print("Split it!", number.lval)
            nlval = int(number.lval / 2)
            nrval = math.ceil(number.lval / 2)
            new = Number(number,nlval,nrval)
            number.left = new
            number.lval = None
#            number.print()
            return number
        
        if(number.right != None):
            rnumber = Find_Left_Split(number.right)
            if(rnumber != None):
                number.right = rnumber
                return number
        elif(number.rval > 9):
#            print("Split it!",number.rval)
            nlval = int(number.rval / 2)
            nrval = math.ceil(number.rval / 2)
            new = Number(number,nlval,nrval)
            number.right = new
            number.rval = None
            return number

        return None

                
def Reduce(number):
    reduce = 1

    while(reduce == 1):
        reduce = 0
        explode = 0
        md = Max_Depth(number.return_print())
        if(md > 5):
            print("Whut?")
            exit()
        # i = Middle_Index(number)

        if(md > 4):
            explode = 1
            reduce = 1
            # Explode
            # Find leftmost pair that needs exploding
            depth = 1
            (lpair,is_left) = Find_Left_Pair(number,depth)
#            lpair.print()

    #       Add_to_Left
            n = lpair
            while(n.parent != None):
                if(n.parent.right == n):
                    # if we were on a right branch, the left path will have our number
                    # either as an lval or the right most down the .right paths.
                    if(n.parent.lval != None):
                        n.parent.lval = n.parent.lval + lpair.lval
                        break
                    elif(n.parent.left != None):
                        go_r_num = n.parent.left
                        while(go_r_num.right != None):
                            go_r_num = go_r_num.right
                        go_r_num.rval = go_r_num.rval + lpair.lval
                        break
                n = n.parent

    #       Add_to_Right
            n = lpair
            while(n.parent != None):
                if(n.parent.left == n):
                    if(n.parent.rval != None):
                        n.parent.rval = n.parent.rval + lpair.rval
                        break
                    elif(n.parent.right != None):
                        go_l_num = n.parent.right
                        while(go_l_num.left != None):
                            go_l_num = go_l_num.left
                        go_l_num.lval = go_l_num.lval + lpair.rval
                        break
                n = n.parent

    #       Replace w/ 0   ##### TODO... this might be a change to 'right'
#            print("is_left",is_left)
            if(is_left):
                lpair.parent.left = None    
                lpair.parent.lval = 0
            else:
                lpair.parent.right = None    
                lpair.parent.rval = 0

        if(explode == 0):
            # check to split big numbers
            # if there's a big number, split it and set reduce = 1
            rnumber = Find_Left_Split(number)
#            print("splitting")
            if(rnumber != None):
                number = rnumber
                reduce = 1

    return number

def Magnitude(number):
    total = 0

    if(number.left != None):
        total += 3 * Magnitude(number.left)
    else:
        total += 3 * number.lval
    
    if(number.right != None):
        total += 2 * Magnitude(number.right)
    else:
        total += 2 * number.rval

    return total


with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    numbers = []
    numbers = Read_Numbers(lines)

    # Part 1
    p1 = False
    if(p1):
        cur_number = numbers[0]
        for i in range(1,len(numbers)):
            cur_number = Add_Numbers(cur_number,numbers[i])

            # Could make a new Max_Depth that works on a Number object
            md = Max_Depth(cur_number.return_print())
            if(md > 4):
                cur_number = Reduce(cur_number)
        
        res = Magnitude(cur_number)
        print("All Magnitude:",res)

    # Part 2
    # We find out that my functions modify the numbers inside the numbers list (oops)
    max = 0
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if(i != j):
                number = Add_Numbers(copy.deepcopy(numbers[i]),copy.deepcopy(numbers[j]))
                md = Max_Depth(number.return_print())
                if(md > 4):
                    number = Reduce(number) 
                res = Magnitude(number)
                if(res > max):
                    max = res
    print("Max Magnitude:",max)
    print("Test should be 3993")


