#!/usr/bin/env python3

import copy

class Universe:
    def __init__(self,p1,p2,p1_wins,p2_wins):
        self.p1 = p1
        self.p2 = p2
        self.p1_wins = p1_wins
        self.p2_wins = p2_wins
    def print(self):
        print("  Player1.win: %i" % self.p1_wins)
        print("  Player2.win: %i" % self.p2_wins)

class Player:
    def __init__(self,pos):
        self.pos = pos
        self.score = 0
    def update_pos(self,total):
        self.pos += total
        rem = self.pos % 10
        self.pos = rem
        if(self.pos == 0):
            self.pos = 10
        return self.pos

testcase = False
if testcase:
    print("TestCase")
    file = "test.txt"
else:
    file = "input.txt"

def get_input(lines):
    first = lines[0].split()
    second = lines[1].split()
    one = int(first.pop())
    two = int(second.pop())
    return (one,two)

# This was modified and no longer works for Part One?
def rolldie(die):
    print("rolldie() may be broken")
    exit(1)
    total = 0
    for i in range(3):
        total += die
        die += 1
        if die == 101:
            die = 1
    return (total,die)

def take_turn(depth,universes,univ,player):
    '''
    The quantum die creates universes with each roll and each player rolls three times.
    That results in 27 possibilities, but we only need to move and add the score once.
    Given the possible totals of rolling a d3, three times, we can reduce our expansion
    from 27 to 7.
    '''
    max_score = 21
    p1_wins = 0
    p2_wins = 0

    # total: num_of_occurances 
    die_values = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    # shutting off a bunch of paths for testing.
#    if(depth == 0 and player == 1):
#        die_values = {3: 1}
#    else:
#        die_values = {3: 1, 4: 3}
    
#    univ.print(depth)

#    print("Start depth:",depth+1)
#    print(univ.p1.pos,univ.p2.pos,univ.p1.score,univ.p2.score,player)

    for val in die_values:

        new_univ = copy.deepcopy(univ)
        if(player == 1):
            # Player 1's Turn
            new_pos = new_univ.p1.update_pos(val)
            new_univ.p1.score += new_pos   #remember, we add position to the score

## NOPE.. this doesn't work because you can come to the same end position from a different die roll
# which results in a different number of wins.  So each tuple is no unique unless we also add the die that was rolled
# to get there.
# Rip out state tracking?
# but first, why is it going down the other half of our short test?

            check_tuple = (new_pos,new_univ.p2.pos,new_univ.p1.score,new_univ.p2.score,1)
#            if(check_tuple in universes):
#                ret_universes[check_tuple] = universes[check_tuple]
#            else:
            if(new_univ.p1.score >= max_score):
#                print("p1 wins",check_tuple,die_values[val])
                p1_wins += die_values[val]
#                p1_wins += 1

            else:
                # keep going deeper
                univ_next = copy.deepcopy(new_univ)

                # it's now player 2's turn
                (p1_ret,p2_ret) = take_turn(depth+1,universes,univ_next,2)

                #print("multiplier",p1_wins,die_values[val]*3)

                p1_wins += p1_ret * die_values[val]
                p2_wins += p2_ret * die_values[val]
                #print("Caught return from p2", p1_wins,p2_wins, "rolled", val)

        else:

            new_pos = new_univ.p2.update_pos(val)
            new_univ.p2.score += new_pos   #remember, we add position to the score

            check_tuple = (new_univ.p1.pos,new_pos,new_univ.p1.score,new_univ.p2.score,2)
#            if(check_tuple in universes):
#                ret_universes[check_tuple] = universes[check_tuple]
#            else:
            if(new_univ.p2.score >= max_score):
#                print("p2 wins",check_tuple)
                p2_wins += die_values[val]

            else:
                # keep going deeper
                univ_next = copy.deepcopy(new_univ)
                # it's now player 2's turn
                (p1_ret,p2_ret) = take_turn(depth+1,universes,univ_next,1)

                #print("multiplier",p1_wins,die_values[val]*3)

                p1_wins += p1_ret * die_values[val]
                p2_wins += p2_ret * die_values[val]
                #print("Caught return from p1", p1_wins,p2_wins,"rolled", val)

    return (p1_wins,p2_wins)



def do_part2(player1,player2):
    '''  
    build a table of known Universes.
    each will be indexed by the current player positions, scores, and current turn order
    the contents will be the number of games won by each player once you
    go down that path.

    so we'll do depth-first to start building that out.
    '''
    # track universes w/ dict of player positions, scores, and who's turn it is
    # p1p,p1s,p2p,p2s,turn  ??  not doing this yet.

    universes = dict()  # or list?

    univ = Universe(player1,player2,0,0)
    universes[(player1.pos,player2.pos,0,0,1)] = univ

    one_total = 0
    two_total = 0

    (one_total, two_total) = take_turn(0,universes,univ,1)



#    for u in ret_universes:
#        one_total += ret_universes[u].p1_wins
#        two_total += ret_universes[u].p2_wins

    print(one_total, two_total)
#    univ_ret.print(0)

    # need to make sure player data is getting deep copied?



with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    (one,two) = get_input(lines)
#    print("Result",one,two)

    player1 = Player(one)
    player2 = Player(two)

    die = 1  # we have a deterministic 100-sided die.
    die_count = 0

    part1 = False
    if(part1):
        while(True):

            (total, die) = rolldie(die)
            die_count += 3
            new_pos = player1.update_pos(total)
            player1.score += new_pos
            if(player1.score >= 1000):
                loser_score = player2.score
                print("Player1 wins")
                break

            (total, die) = rolldie(die)
            die_count += 3
            new_pos = player2.update_pos(total)
            player2.score += new_pos
            if(player2.score >= 1000):
                loser_score = player1.score
                print("Player2 wins")
                break
        
        print("Result:",loser_score * die_count)
    
    do_part2(player1,player2)


    
    





