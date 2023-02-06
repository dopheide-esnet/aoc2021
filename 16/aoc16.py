#!/usr/bin/env python3


def Process_Packet(packet,mode,np,versions):
    '''
    mode and np (number of packets) exist if we're in Mode 1 of an operator packet
    '''

    i = 0
    num_packets = 0
    values = []

    while(i < len(packet) - 1):
        bin_version = "".join(packet[i:i+3])
        bin_type = "".join(packet[i+3:i+6])
        i += 6
        version = int(bin_version, 2)
        versions.append(version)
        type = int(bin_type, 2)
        print("Version/Types:",version,type)
    
        if(type == 4):
            literal = []
            # This is a literal, groups of 5 bits.
            ### AAAHH.. the _binary_ number is padded.  Not the 1,0 prefix
    #        while(packet[i] == '0'):
    #            i += 1  # skip leading zeros
            while(packet[i] == '1'):
    #            print(i,packet[i+1:i+5])
                literal.append(packet[i+1:i+5])
                i += 5
            # now it should be the last segment, starting with a 0
            literal.append(packet[i+1:i+5])
            i += 5

            bin_val = ""
            for l in literal:
                bin_val += "".join(l)
            val = int(bin_val,2)
            values.append(val)
            num_packets += 1
            if(mode == 1):
                if(num_packets == np):
                    print("Values:",values)
                    return (i,values)

            # Can't really do this, might have back-to-back packets.
            # Trailing zeros can be ignored
    #        while(packet[i] == '0'):
    #            i += 1  # skip leading zeros
            # check if it's just trailing zeros, if so, stop and return i
            if('1' not in packet[i:]):
                return (i,values)

#        return i
        else:
            print("Operator")

            m = packet[i]
            i += 1
            if(m == '0'):
                # next 15bits is a number.
                bin_num = "".join(packet[i:i+15])
                num = int(bin_num,2)
                i += 15
                (next_i,next_values) = Process_Packet(packet[i:i+num],0,0,versions)
                i += next_i  
                num_packets += 1
            else:
                # next 11bits is a number.
                bin_num = "".join(packet[i:i+11])
                num = int(bin_num,2)
                i += 11

                ### hhmm.. how to do this based on number of packets...
                # maybe give Process_Packet different modes?
                # Implemented.
                (next_i,next_values) = Process_Packet(packet[i:],1,num,versions)
                i += next_i
                num_packets += 1
            if(mode == 1):
                if(num_packets == np):
                    return (i,values)
            if('1' not in packet[i:]):
                return (i,values)

testcase = True
if testcase:
    file = "test2.txt"
else:
    file = "input.txt"

def Do_It(lines):
    return "Done"

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    input_bytes = bytes.fromhex(lines[0])

    input_binary = "".join(bin(b)[2:].zfill(8) for b in input_bytes)

#    res = Do_It(lines)
#    print("Result",res)

    versions = []
    (idx, values) = Process_Packet(list(input_binary),0,0,versions)

    print("Result:",sum(versions))

    print("Values:",values)






