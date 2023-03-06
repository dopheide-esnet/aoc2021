#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def print_map(map,bounds):
    (oy,ox,my,mx) = bounds
    for y in range(oy,my+1):
#    for y in range(oy,5):
        for x in range(ox,mx+1):
            print(map[y][x],end='')
        print()

def add_border(map,bounds,mode):
    '''
    Adds a border of 'dark' space around the current map.  This should make it easier later
    by always having a valid set of nine characters around a point.
    '''
    (oy,ox,my,mx) = bounds
    map[oy-1] = dict()
    map[my+1] = dict()

    for x in range(ox-1,mx+2):
        map[oy-1][x] = mode
        map[my+1][x] = mode

    for y in range(oy,my+1):
        map[y][ox-1] = mode
        map[y][mx+1] = mode

    return (oy-1,ox-1,my+1,mx+1)
    
def Prep_Input(lines):
    filter = list(lines[0])
    map = {}

    y=0
    for i in range(2,len(lines)):
        line = list(lines[i])
        map[y] = dict()
        for x in range(len(line)):
            map[y][x] = line[x]
        y+=1

    return (filter,map,y-1,len(line)-1)

def filter_image(map,bounds,filter,mode):
    (oy,ox,my,mx) = bounds

    # build a blank output image
    new_map = dict()
    for y in range(oy-1,my+2):
        new_map[y] = dict()
        for x in range(ox-1,mx+2):
            if((mode == '.' and filter[0] == '#')):
                new_map[y][x] = '#'
            elif(mode == '#' and filter[511] == '.'):
                new_map[y][x] = '.'
            else:
                new_map[y][x] = mode

    print_map2(new_map)

    for y in range(oy,my+1):
        for x in range(ox,mx+1):
            # determine binary string for this pixel
            bin_str = ''
            for i in range(y-1,y+2):
                for j in range(x-1,x+2):
                    if(map[i][j] == "."):
                        bin_str += '0'
                    else:
                        bin_str += '1'
#            print(bin_str)
            index = int(bin_str,2)
#            print(index)

#            if(x == ox or y == oy or x == mx or y == my):
                # this is our clear border, don't mess it up if the filter index 0 is a #
#                new_map[y][x] = '.'
#            else:
            new_map[y][x] = filter[index]

    ### todo, grab index value from filter and print in new_map
    return new_map

def count_lit_pixels(map):
    count = 0
    for y in map:
        for x in map[y]:
            if map[y][x] == '#':
                count += 1
    return count

def filter2(map,filter,o,m,mode):
    new_map = dict()
    o -= 1
    m += 1
    
    for y in range(o,m+1):
        if(y not in new_map):
            new_map[y] = dict()
        for x in range(o,m+1):
            binary_string = ''

            for my in range(y-1,y+2):
                if(my not in map):
                    binary_string += mode * 3
                else:  
                    for mx in range(x-1,x+2):
                        if(mx not in map[my]):
                            binary_string += mode
                        elif(map[my][mx] == '.'):
                            binary_string += '0'
                        else:
                            binary_string += '1'

#            print(y,x)
#            print(binary_string)
            new_map[y][x] = filter[int(binary_string,2)]
    return new_map

def print_map2(map):
    for y in map:
        for x in map[y]:
            print(map[y][x],end='')
        print()

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()
    (filter,map,my,mx) = Prep_Input(lines)

    if(0):
        # my and mx should always be equal
        o = 0
        mode = '0'  # the infinite border is in light or dark mode
        map = filter2(map,filter,o,mx,mode)
        mode = '1'
        print_map2(map)

        map = filter2(map,filter,o-1,mx+1,mode)
        mode = '0'
        print_map2(map)

        print("Oooooohh... the infinite border doesn't remain dark if filter[0] == #")

        res = count_lit_pixels(map)
        print("Result",res)

    ''' First Try '''
    mode = '.'
    bounds = (0,0,my,mx) # y,x,my,mx
    bounds = add_border(map,bounds,mode)
    bounds = add_border(map,bounds,mode)

    new_bounds = add_border(map,bounds,mode)
    # we need to start with a 'triple thick' border to make it easy to move around later.

    print_map(map,new_bounds)

    map = filter_image(map,bounds,filter,mode) # use original bounds
    bounds = new_bounds
    print()
    print_map(map,bounds)
    print()

    if((mode == '.' and filter[0] == '#')):
        mode = '#'
    elif(mode == '#' and filter[511] == '.'):
        mode = '.'

    print("Adding border")

    new_bounds = add_border(map,bounds,mode)

#    print_map2(map)

    map = filter_image(map,bounds,filter,mode) # use original bounds
    (oy,ox,my,mx) = bounds
    bounds = (oy-1,ox-1,my+1,mx+1)
    print_map(map,bounds)

    res = count_lit_pixels(map)
    print("Result",res)
