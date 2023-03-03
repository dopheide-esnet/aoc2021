#!/usr/bin/env python3

import re

class Scanner:
    def __init__(self):
        self.beacons = []
        self.beacons_orig = []
        self.flip = None
        self.swap = None
        self.shift = 0
        self.pos = None
        self.parent_scanner = None


testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def Build_Scanners(lines):
    scanners = {}
    for line in lines:
        m = re.search(r'scanner (\d+)',line)
        if(m):
            num = m.group(1)
            scanner = Scanner()
            scanners[int(num)] = scanner
        elif ',' in line:
            coords = line.split(",")
            x = int(coords[0])
            y = int(coords[1])
            z = int(coords[2])
            scanner.beacons.append((x,y,z))
    return scanners

def Check_Beacon_Overlap(scanners,one,two):
    '''
    How?
    '''
    # Okay.. we don't know where s2 is.  Ignore facing for now.
    # Let's take our first s1 beacon and first s2 beacon and Shift all s2 beacons
    # by that different.  Do 3 of them match for the 2D test case?
    # if not, compare s1.1 with s2.2, and so on.
    # Later will need to assume s1.1 isn't one of the matches.
    # Never do more in s1 than  #beacons we have minus #beacons need to match.
    #   (If we haven't found at least one match early on, it's not possible
    # 
    # )

    s1 = scanners[one]
    s2 = scanners[two]

    b = 0  # how many s1 beacons have we looked at.
    count = 1
    for s1b in s1.beacons:
#        print(s1b)

        # remember beacons aren't in any order, have to find the right shift.

        for b2 in range(len(s2.beacons)):  # which s2 beacon do we align this round.
            s2b = s2.beacons[b2]

            # Recall it could be facing OR rotation

            flips = [(1,1,1),(-1,1,1),(1,-1,1),(1,1,-1),(-1,-1,1),(-1,1,-1),(1,-1,-1),(-1,-1,-1)]
            swaps = ["no swap", "x<->y", "x<->z", "y<->z","yzx","zxy"]
#            flips = [(-1,-1,-1)]
#            swaps = ["y<->z"]
            # flips * swaps = 48 different orientations... half have to be effectively equivalent
            # but I'm too lazy to figure out which ones.


            for flip in flips:
                for swap in swaps:

                    (x1,y1,z1) = s1b
                    (x2,y2,z2) = s2b
                    (fx,fy,fz) = flip

                    if(swap == "x<->y"):
                        tmp = x2
                        x2 = y2
                        y2 = tmp
                    elif(swap == "x<->z"):
                        tmp = x2
                        x2 = z2
                        z2 = tmp
                    elif(swap == "y<->z"):
                        tmp = y2
                        y2 = z2
                        z2 = tmp
                    elif(swap == "yzx"):
                        tmp = x2
                        x2 = y2
                        y2 = z2
                        z2 = tmp
                    elif(swap == "zxy"):
                        tmp = x2
                        x2 = z2
                        z2 = y2
                        y2 = tmp
                    # else do nothing in the "no swap" case

                    # calculate shift
                    xd = x1 - (x2 * fx)
                    yd = y1 - (y2 * fy)          
                    zd = z1 - (z2 * fz)

                    tmp_b = []  # temp beacons after shifting.
                    # shift beacons into tmp_b
                    for j in range(len(s2.beacons)):
                        (x2,y2,z2) = s2.beacons[j]

                        if(swap == "x<->y"):
                            tmp = x2
                            x2 = y2
                            y2 = tmp
                        elif(swap == "x<->z"):
                            tmp = x2
                            x2 = z2
                            z2 = tmp
                        elif(swap == "y<->z"):
                            tmp = y2
                            y2 = z2
                            z2 = tmp
                        elif(swap == "yzx"):
                            tmp = x2
                            x2 = y2
                            y2 = z2
                            z2 = tmp
                        elif(swap == "zxy"):
                            tmp = x2
                            x2 = z2
                            z2 = y2
                            y2 = tmp

                        ## TODO so perhaps it's like the origin ones where in half the cases
                        # you don't want to apply the flip back to it?   ugh.

                        newx = xd + (x2 * fx)
                        newy = yd + (y2 * fy)
                        newz = zd + (z2 * fz)

                        tmp_b.append((newx,newy,newz))

                    # check how many beacons match.
                    matches = len(set(s1.beacons) & set(tmp_b))

#                    if(x1 == -447 and y1 == -329 and z1 == 318):
#                        print(f"{count} {swap} {flip} {xd} {yd} {zd} same: {matches}   {tmp_b[0]} {tmp_b[3]}")
                    count+=1

                    # 12 is the provided threshold
                    if(matches >= 12):

#                        print(tmp_b)
                        # do all the stuff to the scanner object
                        scanners[two].beacons_orig = scanners[two].beacons
                        scanners[two].beacons = tmp_b
                        scanners[two].flip = flip
                        scanners[two].swap = swap
                        scanners[two].shift = (xd,yd,zd)
                        scanners[two].parent_scanner = one

#                        print(f"{two} origin {xd},{yd},{zd}")
                        scanners[two].pos = (xd,yd,zd)

                        return (True,scanners[two])

            # TODO figure out the redundant orientations.

    return (False,None)


with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    scanners = Build_Scanners(lines)
    scanners[0].pos = (0,0,0)

    done = []
    proceed = [0]
    # We assume scanner 0 has the correct perspective and we will align everything else to it.

    go = False
    if(go):
        for i in range(len(scanners)):
            for j in range(1,len(scanners)):
                if j not in done and i != j:
                    (res,res_scanner) = Check_Beacon_Overlap(scanners, i, j)
                    if(res):
                        print("We have overlap",i,j)
                        done.append(j)
                        scanners[j] = res_scanner
    else:
        # Do this differently since we all want to align with scanner 0.
        # On proceed with scanners that we have aligned with already.
        # WINNER WINNER!

        while(len(done) < len(scanners)):
            if(len(proceed) == 0):
                print("oops")
                exit()
            i = proceed.pop()

            for j in range(1,len(scanners)):
                if j not in done and j not in proceed and i != j:
                    (res,res_scanner) = Check_Beacon_Overlap(scanners, i, j)
                    if(res):
                        print("We have overlap",i,j)
                        proceed.append(j)
                        scanners[j] = res_scanner

            done.append(i)


all_beacons = []
for scanner in scanners:
    all_beacons.extend(scanners[scanner].beacons)

print(len(set(all_beacons)))

max = 0
for i in range(len(scanners)):
    for j in range(1,len(scanners)):
        (x1,y1,z1) = scanners[i].pos
        (x2,y2,z2) = scanners[j].pos
        md = abs(x1-x2) + abs(y1-y2) + abs(z1-z2)
        if(md > max):
            max = md

print("Max Manhattan:",max)

