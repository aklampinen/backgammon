import copy

class node:
    moves = []
    value = 0
    children = []
    def value(self):
        return value
    def children(self):
        return children
    def moves(self):
        return moves

def position_value(board_array):
    """Finds the value of the position on the board for white, calculated as the difference between the number of points red has to move to win and the number of points white has to, with some modifiers for blots, etc."""
    #Constants which affect the valuation
    blot_penalty = 3
    #End constants
    value = 0

    for i in xrange(len(board_array)):
        if(board_array[i][1] == 1 and i != 0): #Penalties for blots
            value -= blot_penalty*(25.0-i)/24.0
        if(board_array[i][0] == 1 and i != 25): #Penalties for blots
            value += blot_penalty*(i)/24.0
        value += (25-i)*board_array[i][0]
        value -= i*board_array[i][1]
    return value


def build_tree(board_array,die_1_num,die_2_num,doubles,depth_to_search,tree=None):
    """Recursively builds tree of possible moves."""
    #TODO: everything
    if tree == None:
        pass
        #get_white_moves(board_array)
    else:
        pass
    return   

def choose_move(board_array,die_1_num,die_2_num, doubles):
    """Finds the 'best' move in current position according to the value function. Naive 1-ply evaluation."""
    best_value = -1000 #Worse than any possible position's value.
    best_move = []
    curr_pos = copy.deepcopy(board_array)
    num_moves = 2
    if(doubles == True):
        num_moves = 4
    for move in xrange(num_moves):
        temp_best_value = best_value
        temp_best_move = (0,0)
        for i in xrange(len(board_array)):
            for die_num in [die_1_num,die_2_num]:
                if(i-die_num < 0):
                    continue
                if(curr_pos[i][1] == 0):
                    continue
                temp_array = copy.deepcopy(curr_pos)

                if (temp_array[i-die_num][0] > 1 and i-die_num != 0): #If too many opposite color on square (second condition is distinction between bar and bearing off)
                    continue
                if (i-die_num == 0):
                    outside = False
                    for k in xrange(7,26):
                        if(temp_array[k][1] > 0): #If white has a396+*- piece outside home, can't bear off
                            outside = True
                            break
                    if outside == True:
                        print "outside"
                        continue
                if(temp_array[25][1] > 0 and i != 25):#Obligated to move off bar first
                    continue

                #Move the pieces
                temp_array[i][1] -= 1 
                temp_array[i-die_num][1] += 1
                if(temp_array[i-die_num][0] == 1):
                    temp_array[i-die_num][0] -= 1
                    temp_array[0][0] += 1
                temp_value = position_value(temp_array)
                temp_move = (i,i-die_num)
                if(temp_value > temp_best_value):
                    temp_best_value = temp_value
                    temp_best_move = temp_move
 
        if(temp_best_value > best_value):
            best_move.append(temp_best_move)
            best_value = temp_best_value
            curr_pos[temp_best_move[0]][1] -= 1 
            curr_pos[temp_best_move[1]][1] += 1
            if(curr_pos[temp_best_move[1]][0] == 1):
                curr_pos[temp_best_move[1]][0] -= 1
                curr_pos[0][0] += 1
            temp_num = temp_best_move[0]-temp_best_move[1]
            if(temp_num == die_1_num):
                if((doubles == True) and die_2_num == 0):
                    doubles = False
                    die_2_num = die_1_num
                else:
                    die_1_num = 0
            else:
                if((doubles == True) and die_1_num == 0):
                    doubles = False
                    die_1_num = die_2_num
                else:
                    die_2_num = 0
    return best_value,best_move
                
