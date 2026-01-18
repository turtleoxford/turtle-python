import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    cross=33
    nought=2
    board=[0]*12
    wins=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

    # draw blot at specified location with given colour
    def doblot(x,y,col):
        setxy(x*250+250,y*250+175)
        colour(rgb(col))
        blot(70)

    # copy position from one List to another
    def copypos(fromlist,tolist):
        for i in range(len(fromlist)):
            tolist[i]=fromlist[i]

    # evaluate position THISPOS with JM just having moved
    def evaluate(thispos,jm,depth):
        # prepare List NEXTPOS to hold position at next depth
        nextpos=[0]*12
        thispos[9]=0 # THISPOS[9] holds the VALUE of position from JM's point of view
        thispos[10]=-1 # THISPOS[10] holds the MOVE made in the current position
        thispos[11]=depth # THISPOS[11] holds the DEPTH of the analysis
        for i in range(8):
            if (thispos[wins[i][0]]==jm) and (thispos[wins[i][1]]==jm) and (thispos[wins[i][2]]==jm):
                thispos[9]=10-depth # If JM has won, THISPOS[9] (VALUE of position to JM) will be positive
        if thispos[9]==0:
            mover=cross+nought-jm # JM has just moved; MOVER is now choosing a move
            replyscore=-10 # REPLYSCORE, the value of the position to MOVER, should end up higher than this
            m=0
            while (m<9) and (replyscore<1): # Go through every move in turn until a win is found
                if (thispos[m]==0):  # For each empty square M
                    copypos(thispos,nextpos) # Copy the current position to NEXTPOS
                    nextpos[m]=mover # Then add M=MOVER to get new position NEXTPOS
                    evaluate(nextpos,mover,depth+1) # Evaluate NEXTPOS from MOVER's point of view
                    if (nextpos[9]>replyscore): # If value of position to MOVER is greater than REPLYSCORE:
                        replyscore=nextpos[9]     # Record new REPLYSCORE
                        thispos[10]=m             # Record move giving rise to it
                        thispos[11]=nextpos[11]        # Record depth that resulted in it
                m+=1
            if (replyscore!=-10): # If there were any empty squares ...
                thispos[9]=-replyscore # Put value to JM (inverted REPLYSCORE) into THISPOS[9]

    # Main program
    numgames=0
    while 1>0:
        randfirst=numgames%2
        numgames+=1
        blank(lightgreen)
        thickness(10)
        colour(black)
        setxy(375,50)
        drawxy(0,750)
        setxy(625,50)
        drawxy(0,750)
        setxy(125,300)
        drawxy(750,0)
        setxy(125,550)
        drawxy(750,0)
        board=[0]*12
        board[11]=8
        while board[11]>1:
            if randfirst:
                board[10]=randrange(9)
                randfirst=False
            else:
                column = 0
                row = 0
                flag=True
                while (board[column+row*3]!=0) or flag:
                    flag=False
                    # Wait for valid mouse click within bounds
                    while not((get_lmouse()>0) and (get_clickx()>=125) and (get_clickx()<=875) and (get_clicky()>=50) and (get_clicky()<=800)):
                        detect("click", 0)
                    column=(get_clickx()-125)//250
                    row=(get_clicky()-50)//250
                    # Wait for mouse button to be released before next click
                    while get_lmouse()>0:
                        update()
                doblot(column,row,cross)
                board[column+row*3]=cross
                evaluate(board,cross,0)
            if board[10]!=-1:
                doblot(board[10]%3,board[10]//3,nought)
                board[board[10]]=nought
        setxy(350,850)
        colour(black)
        if board[9]==0:
            display('  Draw!  ',4,60)
        else:
            display('  I win!  ',4,60)
        pause(2500)