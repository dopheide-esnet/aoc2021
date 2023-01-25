#!/usr/bin/env python3

import re

class Board:
    def __init__(self, rows):
        self.rows = rows # do something better


testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def Boards(lines):
    '''
    Generate the board objects.
    Although, my grandma would've corrected us and said these are bingo 'cards'
    '''
    boards = []
    while(1):
        board = []
        for i in range(5):
            m = re.search(r'(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)',lines.pop(0))
            if(m):
                row = [ {m.group(1): 0},
                        {m.group(2): 0},
                        {m.group(3): 0},
                        {m.group(4): 0},
                        {m.group(5): 0} ] 
                board.append(row)
            else:
                print("Regex error")
                exit()
        boards.append(board)
        if(len(lines)> 1):
            lines.pop(0)  # pop a blank line.
        else:
            break

    return boards

def Mark_It(boards,num):
    # for each board
    for b in range(len(boards)):
        # look at each row
        for r in range(len(boards[b])):
            # look at each column
            for c in range(len(boards[b][r])):
                if(num in boards[b][r][c]):
                    boards[b][r][c] = {num: 1}


def Check_Bingo(boards):
    for b in range(len(boards)):
        col_match = [1,1,1,1,1]
        row_match = [1,1,1,1,1]
        r = 0
        for row in boards[b]:
            i = 0
            for c in row:
                for key in c.keys():
                    if(c[key] == 0):
                        row_match[r] = 0
                        col_match[i] = 0
                i += 1
            r += 1              
        if(1 in col_match or 1 in row_match):
            print("Board matched!")
            return b

## TODO, something still wrong here?
# oh crap, a single number could expire multiple boards...

    return -1

def Score(board,num):
    total = 0
    for row in board:
        for c in row:
            for key in c.keys():
                if(c[key] == 0):
                    total += int(key)  # don't forget the int conversion!
    total *= int(num)

    return total

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    call_numbers = lines.pop(0).split(',')
    lines.pop(0)  # get rid of the next empty line
    boards = Boards(lines)

# Part 1
#    for num in call_numbers:
#        Mark_It(boards,num)
#        b = Check_Bingo(boards)
#        if(b != -1):
#            print(boards[b])
#            break

    for num in call_numbers:
        Mark_It(boards,num)
        # more than one board could match on a single nunber.
        b = Check_Bingo(boards)
        while(b != -1):
            if(len(boards) == 1):
                print("Last board matched")
                score = Score(boards[b],num)
                print("Score:",score)
                exit()
            else:
                boards.pop(b)
                b = Check_Bingo(boards)

    print(boards)

    score = Score(boards[b],num)   # num that was just called
    print("Score:",score)

    # for later math, recall we never converted any of these to integers.



