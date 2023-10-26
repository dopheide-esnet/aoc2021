#!/usr/bin/env python3

import re

testcase = True
if testcase:
    print("Doing Small Test.txt")
    file = "small_test.txt"
else:
    file = "input.txt"

def Do_Input(lines):
    # on x=-12..35,y=6..50,z=-50..-2
    instructions = []
    for line in lines:
        m = re.search(r'^(on|off) x=([\-0-9]+)\.\.([\-0-9]+),y=([\-0-9]+)\.\.([\-0-9]+),z=([\-0-9]+)\.\.([\-0-9]+)',line)
        #x=([\-0-9])\.\.([\-0-9]),y=([\-0-9])\.\.([\-0-9]),z=([\-0-9])\.\.([\-0-9])',line)
        if(m):
            action = m.group(1)
            x_min = int(m.group(2))
            x_max = int(m.group(3))
            y_min = int(m.group(4))
            y_max = int(m.group(5))
            z_min = int(m.group(6))
            z_max = int(m.group(7))
            instructions.append((action, x_min, x_max, y_min, y_max, z_min, z_max))

    # convert to int

    return instructions

def process1(space, instructions):

    for i in range(len(instructions)):
        (action, x_min, x_max, y_min, y_max, z_min, z_max) = instructions[i]

        # TODO, need to check if the instructions are in range
        if(not (x_min > 50 or x_max < -50 or y_min > 50 or y_max < -50 or z_min > 50 or z_max < -50)):

            print(instructions[i])
            for x in range(x_min,x_max+1):
                for y in range(y_min,y_max+1):
                    for z in range(z_min,z_max+1):
                        if(action == 'on'):
                            space[(x,y,z)] = 1
                        else:
                            if (x,y,z) in space:
                                del space[(x,y,z)]
    return


def get_extents(squares):
    (ac, x1, x2, y1, y2) = squares[0]
    for s in range(1,len(squares)):
        (ac,i1,i2,j1,j2) = squares[s]
        if(i1 < x1):
            x1 = i1
        if(i2 > x2):
            x2 = i2
        if(j1 < y1):
            y1 = j1
        if(j2 > y2):
            y2 = j2

    return (x1,x2,y1,y2)

def get_zextents(instructions):
    (ac, x1, x2, y1, y2, z1, z2) = instructions[0]
    for i in range(1,len(instructions)):
        (ac, i1, i2, j1, j2, k1, k2) = instructions[i]
        if(k1 < z1):
            z1 = k1
        if(k2 > z2):
            z2 = k2
    return(z1,z2)

def print_squares(squares,extents):
    # doesn't need to be super efficient, only for testing
    field = []
    (minx,maxx,miny,maxy) = extents
    for y in range(miny,maxy+1):
        line = []
        for x in range(minx,maxx+1):
            line.append(' ')
        field.append(line)

    for s in range(len(squares)):
        (action,x1,x2,y1,y2) = squares[s]

        for y in range(y1,y2+1):
            for x in range(x1,x2+1):
                field[y-miny][x-minx] = str(s%10)

#    print(field)
    for y in range(len(field)):
        for x in range(len(field[y])):
            print(field[y][x],end='')
        print()

def add_square(squares,stuple):
    ''' except most are probably rectangles '''
    (action,x1,x2,y1,y2) = stuple

    ## split up the addition if necessary and then pass those 

#    print("dammit")
#    exit()
    # TODO.. shit... 
    # if we split into new squares, we have to stop processing the current stuple.

    remove = False
    ignore = False
    new_squares = []
    for s in range(len(squares)):
        (saction,sx1,sx2,sy1,sy2) = squares[s]
#        print("Checking",(saction,sx1,sx2,sy1,sy2))
        new_squares = []
        edit = False

        # Case 0:  No overlap with this square.
        if(x1 > sx2 or x2 < sx1 or y1 > sy2 or y2 < sy1):
            continue

        # Case 1 (bottom right overlap)
        # doesn't account for equal edges yet, handle that with a different case
        if(x1 > sx1 and x1 <= sx2 and x2 > sx2 and
           y1 > sy1 and y1 <= sy2 and y2 > sy2):
            print("Case1")
            # So we need to skip the overlap and break it into two squares

            # right square
            rx1 = sx2 + 1
            new_squares.append(('on',rx1,x2,y1,y2))

            # bottom square
            rx2 = sx2
            ry1 = sy2+1
            new_squares.append(('on',x1,rx2,ry1,y2))

        # Case 2 (top right overlap)
#        elif(x1 > sx1 and x1 < sx2 and x2 > sx2 and
#           y1 < sy1 and y1 < sy2 and y2 < sy2):
        elif(x1 > sx1 and x1 <= sx2 and x2 > sx2 and
           y1 < sy1 and y1 < sy2 and y2 <= sy2):
            print("Case2")

            # right square
            rx1 = sx2 + 1
            new_squares.append(('on',rx1,x2,y1,y2))

            # top square
            rx2 = sx2
            ry2 = sy1-1
            new_squares.append(('on',x1,rx2,y1,ry2))

        # Case 3 (bottom left overlap)
        elif(x1 < sx1 and x2 <= sx2 and x2 < sx2 and
           y1 > sy1 and y1 <= sy2 and y2 > sy2):
            print("Case3")

            # left square
            rx2 = sx1 - 1
            new_squares.append(('on',x1,rx2,y1,y2))

            # bottom square
            rx1 = sx1
            ry1 = sy2+1
            new_squares.append(('on',rx1,x2,ry1,y2))

        # Case 4 (top left overlap)
        elif(x1 < sx1 and x1 <= sx2 and x2 < sx2 and
           y1 < sy1 and y1 < sy2 and y2 <= sy2):
            print("Case4")

            # left square
            rx2 = sx1 - 1
            new_squares.append(('on',x1,rx2,y1,y2))

            # top square
            rx1 = sx1
            ry2 = sy1-1
            new_squares.append(('on',rx1,x2,y1,ry2))

        # Case 5 (top inclusion)
        elif(x1 >= sx1 and x2 <= sx2 and
           y1 < sy1 and y2 >= sy1 and y2 < sy2):
            print("Case5")

            # top square
            ry2 = sy1-1
            new_squares.append(('on',x1,x2,y1,ry2))

        # Case 6 (bottom inclusion)
        elif(x1 >= sx1 and x2 <= sx2 and
           y1 > sy1 and y1 <= sy2 and y2 > sy2):
            print("Case6")

            # top square
            ry1 = sy2+1
            new_squares.append(('on',x1,x2,ry1,y2))

        # Case 7 (right inclusion)
#        elif(x1 > sx1 and x1 < sx2 and x2 > sx2 and
        elif(x1 > sx1 and x1 <= sx2 and x2 > sx2 and
           y1 >= sy1 and y2 <= sy2):
            print("Case7")

            # top square
            rx1 = sx2+1
            new_squares.append(('on',rx1,x2,y1,y2))

        # Case 8 (left inclusion)
        elif(x1 < sx1 and x2 >= sx1 and x2 < sx2 and
           y1 >= sy1 and y2 <= sy2):
            print("Case8",stuple)
            # top square
            rx2 = sx1-1
            new_squares.append(('on',x1,rx2,y1,y2))

        # Case 9 (top overlap)
        elif(x1 <= sx1 and x2 >= sx2 and
           y1 <= sy1 and y2 >= sy1 and y2 < sy2):
            print("Case9",stuple)

            # modify the current squares[s]
            edit = True
            squares[s] = ('on',sx1,sx2,y2+1,sy2)

        # Case 10 (bottom overlap)
        elif(x1 <= sx1 and x2 >= sx2 and
           y1 > sy1 and y1 <= sy2 and y2 >= sy2):
            print("Case10")

            # modify the current squares[s]
            edit = True
            squares[s] = ('on',sx1,sx2,sy1,y1-1)

        # Case 11 (right overlap)
        elif(x1 > sx1 and x1 <= sx2 and x2 >= sx2 and
           y1 <= sy1 and y2 >= sy2):
            print("Case11")

            # modify the current squares[s]
            edit = True
            squares[s] = ('on',sx1,x1-1,sy1,sy2)

        # Case 12 (left overlap)
        elif(x1 <= sx1 and x2 >= sx1 and x2 < sx2 and
           y1 <= sy1 and y2 >= sy2):
            print("Case12")

            # modify the current squares[s]
            edit = True
            squares[s] = ('on',x2+1,sx2,sy1,sy2)

        # Case 13 (bissect vertical)
        elif(x1 > sx1 and x2 < sx2 and
           y1 < sy1 and y2 > sy2):
            print("Case13")

            # top square
            new_squares.append(('on',x1,x2,y1,sy1-1))
            # bottom square
            new_squares.append(('on',x1,x2,sy2+1,y2))

        # Case 13 (bissect thin top)
        elif(x1 > sx1 and x2 < sx2 and
           y1 < sy1 and y2 == sy2):
            print("Case13b")
            new_squares.append(('on',x1,x2,y1,sy2-1))

        # Case 13 (bissect thin bottom)
        elif(x1 > sx1 and x2 < sx2 and
           y1 == sy1 and y2 > sy2):
            print("Case13b")
            new_squares.append(('on',x1,x2,y1,sy2-1))

        # Case 14 (bissect horizontal)
        elif(x1 < sx1 and x2 > sx2 and
           y1 > sy1 and y2 < sy2):
            print("Case14")

            # left square
            new_squares.append(('on',x1,sx1-1,y1,y2))
            # right square
            new_squares.append(('on',sx2+1,x2,y1,y2))

        # Case 14b (bissect thin left)
        elif(x1 < sx1 and x2 == sx2 and
             y1 > sy1 and y2 < sy2):
            print("Case 14b")
            new_squares.append(('on',x1,sx2-1,y1,y2))

        # Case 14c (bissect thin right)
        elif(x1 == sx1 and x2 > sx2 and
             y1 > sy1 and y2 < sy2):
            print("Case 14c")
            new_squares.append(('on',sx1+1,x2,y1,y2))


        # Case 15 (total overlap)
        elif(x1 <= sx1 and x2 >= sx2 and
           y1 <= sy1 and y2 >= sy2):
            print("Case15")

            # break and remove the current squares[s]
            # then try again.
            edit = True
            remove = True
            break

        # Case 16 (totally inside can be ignored when adding)
        elif(x1 >= sx1 and x2 <= sx2 and
           y1 >= sy1 and y2 <= sy2):
            print("Case16")
            ignore = True
            return # ?

        # If there are new_squares we need to stop processing the original
        # square since it's been broken up.
        if(len(new_squares) > 0):
            break
        elif(edit == False):
            print("overlap of some kind, but no match?",stuple)
            exit(1)

    if(remove == True):
        squares.remove(squares[s])
        # continue processing this square against the modified list.
        # (inefficient, will re-check previous squares, but shouldn't be too bad)
        add_square(squares,stuple)

    # If we got here with no overlap with any squares, we just add it.
    elif len(new_squares) == 0:
        squares.append(stuple)
    else:
        for ns in range(len(new_squares)):
            add_square(squares,new_squares[ns])

    return


def delete_square(squares,stuple):
    ''' except most are probably rectangles '''
    (action,x1,x2,y1,y2) = stuple

    # We'll need to break up existing squares and add smaller ones.

    # New smaller squares will be added to the end of the list, but we know they're 'clear'
    # so we don't have to re-interate over them.
    for s in range(len(squares)):
        (sa,sx1,sx2,sy1,sy2) = squares[s]

        # top left
        if(x1 <= sx1 and x2 < sx2 and
           y1 <= sy1 and y2 < sy2 ):
            squares[s] = ('on',x2+1,sx2,sy1,sy2) # these are still 'on'
            squares.append(('on',sx1,sx2,y2+1,sy2))

    return


with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    instructions = Do_Input(lines)
#    print(instructions)

    space = {}
    part1 = False
    if(part1):
        process1(space,instructions)
        print(len(space))

    # Let's do this one 2D plane at a time.
#    squares = [('on',-2,2,-2,2),
#               ('on',0,3,0,3)]

    # run lame tests
    if(False):
        squares = [('on',-2,2,-2,2)]
        add_square(squares,('on',0,3,0,3))  # Case 1
        add_square(squares,('on',0,3,-3,1))  # Case 2
        add_square(squares,('on',-4,1,0,4))  # Case 3
        add_square(squares,('on',-4,1,-3,1)) # Case 4
        add_square(squares,('on',-2,1,-3,0))  # Case 5
        add_square(squares,('on',-1,2,0,4))  # Case 6
        add_square(squares,('on',0,4,-1,1))  # Case 7
        add_square(squares,('on',-4,-2,-2,1)) # Case 8
        add_square(squares,('on',-3,3,-3,0))   # Case 9
        add_square(squares,('on',-3,3,0,3))   # Case 10
        add_square(squares,('on',0,3,-3,3)) # Case 11
        add_square(squares,('on',-3,0,-3,3)) # Case 12
        add_square(squares,('on',-1,0,-3,3)) # Case 13
        add_square(squares,('on',-3,3,-1,0)) # Case 14
        add_square(squares,('on',-3,3,-2,2)) # Case 15
        add_square(squares,('on',-2,0,-2,0)) # Case 16
        # Inside squares, can be totally ignored for the add'ing case.
    elif(True):
        print("Run Delete tests")

        squares = [('on',-2,2,-2,2)]
        delete_square(squares,('off',-3,0,-3,0))
        # Do in reverse?  Test each square against the delete 'target'
        # since we'll need to delete squares from our interable...


    else:
        squares=[]
        (z_start,z_end) = get_zextents(instructions)
        print("Z",z_start,z_end)
        volume = 0
        for z in range(z_start,z_end+1):
            print("Z:",z)

            for i in range(len(instructions)):
    #            print(i)
                (action,x1,x2,y1,y2,z1,z2) = instructions[i]
                # check if instructions is within current Z level
                if(z >= z1 and z <= z2 ):
                    if(action == 'on'):
                        add_square(squares,('on',x1,x2,y1,y2))
# TODO
#                    else:
#                        delete_square 

            # Calculate Volume.
            # Remember, '0' is a cube, not just a coordinate
            for s in range(len(squares)):
                (a,x1,x2,y1,y2) = squares[s]
                volume += (x2 - x1 + 1) * (y2 - y1 + 1)
    #            print("square",squares[s],volume)
        print("Volume with only adds:",volume)


# Then go through all the deletion scenarios

    # Potential efficiency gain:
    # We can cache the volume of a slice if the same set of instructions would be repeated
    # in the next slice.


    extents = get_extents(squares)
    print("E:",extents)
    print_squares(squares,extents)

