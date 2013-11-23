from Tkinter import *
from tkFont import Font
from time import sleep
import copy
import random
import backgammon_AI


board_array = [[0,0] for i in xrange(0,26)] #The first coordinate gives number of red draughts on point, second gives number of white. Points are indexed from bottom right around the board, with black's goal & red's bar being point 0, red's goal and black's bar being point 25, 
red_draughts = []
white_draughts = []

#Stuff for dragging and dropping draughts
click_offset = [0,0]
old_point = -1

#Numbers showing on dice
die_1_num = 0
die_2_num = 0
doubles = False

#Turn stuff
red_turn = True


def roll():
    """Rolls the dice"""
    global die_1_num, die_2_num, doubles
    global die_1, die_2
    die_1_num = random.randrange(1,7)
    die_2_num = random.randrange(1,7)
    print die_1_num,die_2_num
    if(die_1_num == die_2_num):
        doubles = True
    else:
        doubles = False
    update_dice()

def move_draught_begin(event):
    """Deals with the headaches of beginning moving the draught."""
    global red_draughts, white_draughts
    global board_array
    global click_offset
    global old_point
    draught = board.find_withtag(CURRENT)[0]
    click_offset = [event.x-board.coords(draught)[0],event.y-board.coords(draught)[1]] #How far off the click is from the coordinates of the draught it's moving
    bottom = (event.y-click_offset[1] >= board_height//2)
    point_left_edges = [board_divisions*i for i in xrange(0,15) if i != 7]
    if bottom == False:
        if(event.x-click_offset[0] == 7*board_divisions): #If on the white bar
            old_point = 25
        else:
            old_point = 12+point_left_edges.index(min(point_left_edges, key=lambda x:abs(x-event.x+click_offset[0])))
    else:
        if(event.x-click_offset[0] == 7*board_divisions): #If on the red bar
            old_point = 0
        else:
            old_point = 13-point_left_edges.index(min(point_left_edges, key=lambda x:abs(x-event.x+click_offset[0])))    


def move_draught(event):
    """Deals with the headaches of moving the draught."""
    global red_turn
    if(red_turn == False):
        return
    draught = board.find_withtag(CURRENT)[0]
    board.coords(draught,event.x-click_offset[0],event.y-click_offset[1],event.x-click_offset[0]+board_divisions,event.y-click_offset[1]+board_divisions)

def move_draught_end(event):
    """Deals with the headaches of ending moving the draught & checking legality of move."""
    global red_draughts, white_draughts
    global board_array
    global old_point
    global die_1_num, die_2_num, doubles
    draught = board.find_withtag(CURRENT)[0]
    #Figure out which point they want to put it on
    bottom = (event.y-click_offset[1] >= board_height//2)
    point_left_edges = [board_divisions*i for i in xrange(0,15) if i != 7]
    is_red = draught in red_draughts
    if bottom == False:
        new_point = 12+point_left_edges.index(min(point_left_edges, key=lambda x:abs(x-event.x+click_offset[0])))
    else:
         new_point = 13-point_left_edges.index(min(point_left_edges, key=lambda x:abs(x-event.x+click_offset[0])))   
    #Check legality
    if(board_array[new_point][1] > 1 and is_red) or (board_array[new_point][0] > 1 and not is_red): #if too many opposite color on square
        draw_draughts()
        return
    if(board_array[0][0] > 0 and is_red and old_point != 0)or(board_array[25][1] > 0 and not is_red and old_point != 25):#Obligated to move off bar first
        draw_draughts()
        return
    if(new_point == 0 and not is_red): #if white trying to bear off
        for i in xrange(7,26):
            if(board_array[i][1] > 0): #If white has a piece outside home, can't bear off
                draw_draughts()
                return
    if(new_point == 25 and is_red): #if red trying to bear off
        for i in xrange(0,18):
            if(board_array[i][0] > 0): #If red has a piece outside home, can't bear off
                draw_draughts()
                return        
 
    if(new_point-old_point == die_1_num and is_red) or (old_point-new_point == die_1_num and not is_red):
        if(doubles == False) or (die_2_num != 0):
            die_1_num = 0
        else: 
            die_2_num = die_1_num
            doubles = False
    elif(new_point-old_point == die_2_num and is_red) or (old_point-new_point == die_2_num and not is_red):
        if(doubles == False) or (die_1_num != 0):
            die_2_num = 0
        else: 
            die_1_num = die_2_num
            doubles = False
    else: #Can't move there on this roll
        draw_draughts()
        return
    update_dice()
    #Update board_array
    if is_red:
        board_array[old_point][0] -= 1
        board_array[new_point][0] += 1
        if(board_array[new_point][1] == 1): #Handle hits
            board_array[new_point][1] -= 1
            board_array[25][1] += 1
    else:
        board_array[old_point][1] -= 1
        board_array[new_point][1] += 1
        if(board_array[new_point][0] == 1): #Handle hits
            board_array[new_point][0] -= 1
            board_array[0][0] += 1

    draw_draughts()
    if(die_1_num == 0 and die_2_num == 0):
        comp_turn()
    
    
   

def draw_draughts():
    """Draws the draughts on the board from the board array"""
    global red_draughts
    global white_draughts
    global board_array
    if(red_draughts == []):
        red_draughts = [board.create_oval(0,0,board_divisions,board_divisions,fill="red") for i in xrange(0,15)]
        white_draughts = [board.create_oval(0,0,board_divisions,board_divisions,fill="white")for i in xrange(0,15)]
        #And create event handlers for dragging these
        for draught in red_draughts:
            board.tag_bind(draught, "<Button-1>", move_draught_begin)
            board.tag_bind(draught, "<B1-Motion>", move_draught)
            board.tag_bind(draught, "<ButtonRelease-1>", move_draught_end)
        for draught in white_draughts:
            board.tag_bind(draught, "<Button-1>", move_draught_begin)
            board.tag_bind(draught, "<B1-Motion>", move_draught)
            board.tag_bind(draught, "<ButtonRelease-1>", move_draught_end)

    unmoved_red = list(red_draughts)
    unmoved_white = list(white_draughts)
    red_draughts = []
    white_draughts = []
    print board_array
    for i in xrange(1,len(board_array)-1): #Handle Points, ends and bar handled as special cases
        #Calculate where left side of draughts should be, and whether on top or bottom
        if i <= 6:
            left_side = board_divisions*(8+(6-i))
            bottom = True
        elif i <= 12:
            left_side = board_divisions*(1+(12-i))
            bottom = True
        elif i <= 18:
            bottom = False
            left_side = board_divisions*(1+(i-13))
        else:   
            bottom = False
            left_side = board_divisions*(8+(i-19))
        #Move red draughts to right places
        for j in xrange(board_array[i][0]):
            temp = unmoved_red.pop()
            if(bottom == True):
                board.coords(temp,left_side+board_divisions//10*(j//5),board_divisions*(9-(j%5)),left_side+board_divisions+board_divisions//10*(j//5),board_divisions*(10-(j%5)))
            else:
                board.coords(temp,left_side+board_divisions//10*(j//5),board_divisions*(j%5),left_side+board_divisions+board_divisions//10*(j//5),board_divisions*((j%5)+1))
            red_draughts.append(temp)
        #Now white
        for j in xrange(board_array[i][1]):
            temp = unmoved_white.pop()
            if(bottom == True):
               board.coords(temp,left_side+board_divisions//10*(j//5),board_divisions*(9-(j%5)),left_side+board_divisions+board_divisions//10*(j//5),board_divisions*(10-(j%5)))
            else:
                board.coords(temp,left_side+board_divisions//10*(j//5),board_divisions*(j%5),left_side+board_divisions+board_divisions//10*(j//5),board_divisions*((j%5)+1))
            white_draughts.append(temp)
    #Handle white end, red bar
    #Move red draughts to right places on bar
    for j in xrange(board_array[0][0]):
        temp = unmoved_red.pop()
        board.coords(temp,7*board_divisions+board_divisions//10*(j//4),board_divisions*(9-(j%4)),7*board_divisions+board_divisions+board_divisions//10*(j//4),board_divisions*(10-(j%4)))
        red_draughts.append(temp)

    #Now white to places in goal
    for j in xrange(board_array[0][1]):
        temp = unmoved_white.pop()
        board.coords(temp,14*board_divisions+board_divisions//10*(j//4),board_divisions*(9-(j%4)),14*board_divisions+board_divisions+board_divisions//10*(j//4),board_divisions*(10-(j%4)))
        white_draughts.append(temp)
    #Handle red end, white
    #Move white draughts to right places on bar

    for j in xrange(board_array[25][1]):
        temp = unmoved_white.pop()
        board.coords(temp,7*board_divisions+board_divisions//10*(j//4),board_divisions*(j%4),7*board_divisions+board_divisions+board_divisions//10*(j//4),board_divisions*((j%4)+1))
        white_draughts.append(temp)

    #Now red to places in goal
    for j in xrange(board_array[25][0]):
        temp = unmoved_red.pop()
        board.coords(temp,14*board_divisions,board_divisions*j,15*board_divisions,board_divisions*(j+1))
        board.coords(temp,14*board_divisions+board_divisions//10*(j//4),board_divisions*(j%4),14*board_divisions+board_divisions+board_divisions//10*(j//4),board_divisions*((j%4)+1))
        red_draughts.append(temp)
    if(board_array[25][0] == 15):
        print "You win!"
        
def comp_turn():
    """Handles computer's turn, deactivates moving, calls AI, etc."""
    global red_turn,board_array,die_1_num,die_2_num
    roll()
    red_turn = False
    value,move = backgammon_AI.choose_move(board_array,die_1_num,die_2_num,doubles)
    print value,move
    if(value != -1000):
        for sub_move in move:
            board_array[sub_move[0]][1] -= 1
            board_array[sub_move[1]][1] += 1
            if(board_array[sub_move[1]][0] == 1): #Handle hits
                board_array[sub_move[1]][0] -= 1
                board_array[0][0] += 1
    die_1_num = 0
    die_2_num = 0
    update_dice()
    draw_draughts()
    red_turn = True

def reset(): 
    """Resets the board state"""
    global board_array
    global die_1_num,die_2_num
    board_array = [[0,0] for i in xrange(0,26)]
    board_array[1] = [2,0]
    board_array[24] = [0,2]
    board_array[6] = [0,5]
    board_array[19] = [5,0]
    board_array[8] = [0,3]
    board_array[17] = [3,0]
    board_array[12] = [5,0]
    board_array[13] = [0,5]

    die_1_num = 0
    die_2_num = 0
    update_dice()
    draw_draughts()

def update_dice(): #Update numbers on dice
    global die_1,die_2,die_1_num,die_2_num
    die_1.config(text=str(die_1_num))
    die_2.config(text=str(die_2_num))


#Seed the randomd number generator
random.seed()
#Build the interface & visible board
#Constants:
board_width = 990 #Geometry will work nicer if multiple of 15
board_height = 10*board_width//15
board_divisions = board_width//15
khaki = "#f5deb3" #Background for board
brown = "#8b4513" #Point color
#Tkinter stuff
root = Tk()
board_frame = Frame(width=board_width+100,height=board_height+100,relief=SUNKEN,bd=1)
board_frame.pack(side="left")
dice_frame = Frame(width=100,height=100,relief=SUNKEN,bd=1)
dice_frame.pack(side="top")
pass_button = Button(dice_frame, text="Pass", command=comp_turn)
pass_button.pack(side="bottom",fill=X,expand=1)
roll_button = Button(dice_frame, text="Roll", command=roll)
roll_button.pack(side="bottom",fill=X,expand=1)

die_1 = Label(dice_frame,text="6",font=Font(size=30))
die_1.pack(side="left")
die_2 = Label(dice_frame,text="6",font=Font(size=30))
die_2.pack(side="right")

reset_button = Button(root, text="New Game",command=reset)
reset_button.pack(side="right")
#Set up the board
board = Canvas(board_frame,width=board_width,height=board_height,background=khaki)
board.pack()

#Set up board graphics
#Edges
board.create_rectangle(0,0,board_divisions,6*board_height//15,fill="black")
board.create_rectangle(0,9*board_height//15,board_divisions,board_height,fill="black")
board.create_rectangle(14*board_divisions,0,board_width,6*board_height//15,fill="black")
board.create_rectangle(14*board_divisions,9*board_height//15,board_width,board_height,fill="black")
#Middle bar
board.create_rectangle(7*board_divisions,0,8*board_divisions,7*board_height//15,fill="black")
board.create_rectangle(7*board_divisions,8*board_height//15,8*board_divisions,board_height,fill="black")
#Points
for i in xrange(1,14):
    if(i == 7):
        continue
    board.create_polygon(i*board_divisions,0,(i+1)*board_divisions,0,((2*i+1)*board_divisions)//2,6*board_height//15,fill=brown)
    board.create_polygon(i*board_divisions,board_height,(i+1)*board_divisions,board_height,((2*i+1)*board_divisions)//2,9*board_height//15,fill=brown)
#phew, done with static stuff, let's start rendering
root.mainloop()






