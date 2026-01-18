import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    # Set size of canvas
    width=50
    height=50
    empty=green

    # Function: is colour c happy at (x,y)?
    def happy(x,y,c):
        like=0
        unlike=0
        for i in range(-1,2):
            for j in range(-1,2):
                if (i!=0) or (j!=0):
                    neighbour=pixcol(x+i,y+j)
                    if neighbour!=empty:
                        if neighbour==c:
                            like+=1
                        else:
                            unlike+=1
        return (like>=unlike-1)

    # Set up initial canvas and map
    canvas(-1,-1,width+2,height+2)
    noupdate()
    blank(empty)
    for i in range(width):
        for j in range(height):
            if randrange(25)==0:
                pixset(i,j,empty)
            else:
                if (i+j)%2==0:
                    pixset(i,j,red)
                else:
                    pixset(i,j,blue)
    # Pause to show initial map
    pause(2000)
    while get_key_sym()!="Escape":
        noupdate()
        this=empty
        # Find an unhappy cell
        while (this==empty) or (happy(tryi,tryj,this)):
            tryi=randrange(width)
            tryj=randrange(height)
            this=pixcol(tryi,tryj)
        pixset(tryi,tryj,empty)
        # Find an empty cell where they'll be happy
        while (pixcol(tryi,tryj)!=empty) or not(happy(tryi,tryj,this)):
            tryi=randrange(width)
            tryj=randrange(height)
        pixset(tryi,tryj,this)
        update()