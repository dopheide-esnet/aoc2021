#!/usr/bin/env python3

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

def Get_Best(lines):
    # Initialize our output structure
    output = []
    for i in range(len(lines[0])):
        output.append({'one':0,'zero':0})

    for line in lines:
        for i in range(len(line)):
            if(line[i] == '1'):   # it's a string, not an int
                output[i]['one'] += 1
            else:
                output[i]['zero'] += 1
    return output

def Get_Power(lines):
    '''
    Split each binary string to count the 1's and 0's in each place.
    '''

    output = Get_Best(lines)

    gamma = ''
    epsilon = ''
    for i in range(len(output)):
        if(output[i]['one'] > output[i]['zero']):
            gamma += '1'
            epsilon += '0'
        else:
            gamma += '0'
            epsilon += '1'

    g_num = int(gamma,2)
    e_num = int(epsilon,2)

#    print(output)

    return (g_num,e_num)


def Get_Life(lines):
    output = Get_Best(lines)

    orig_lines = lines

    current = []
    i = 0
    while(len(lines) > 1):
        output = Get_Best(lines)  # re-count based on the current set of lines
        current = []
        if(output[i]['one'] >= output[i]['zero']):  # If 0 and 1 are equally common, select 1.
            val = '1'
        else:
            val = '0'

        for line in lines:
            bits = list(line)
            if(bits[i] == val):
                current.append(line) # keep it.

        lines = current
        i += 1

    oxy = int(lines[0],2)

    # could probably do this all in one loop, but not super worried about efficiency right now
    lines = orig_lines
    i = 0
    while(len(lines) > 1):
        output = Get_Best(lines)  # re-count based on the current set of lines
        current = []
        if(output[i]['one'] < output[i]['zero']):  # If 0 and 1 are equally common, select 0.
            val = '1'
        else:
            val = '0'

        for line in lines:
            bits = list(line)
            if(bits[i] == val):
                current.append(line) # keep it.

        lines = current
        i += 1

    co2 = int(lines[0],2)

    return (oxy,co2)



with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    (gamma, epsilon) = Get_Power(lines)
    print("Gamma:",gamma)
    print("Epsilon:",epsilon)
    print("Power:",gamma*epsilon)
    
    (oxy, co2) = Get_Life(lines)
    print("Oxygen:",oxy)
    print("CO2:",co2)
    print("Life:",oxy * co2)




