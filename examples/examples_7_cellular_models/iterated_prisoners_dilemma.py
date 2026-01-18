import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    # Set dimensions and number of iterations
    width=40
    height=40
    n=10

    # Define utilities list based on payoffs
    util=[0,3*n,3*n,3*n,0,5*n,n+4,0,0,0,0,0,n,0,n-1]

    # Function to calculate utility for each cell and store within colour code
    def utility(x,y):
        this=pixcol(x,y)&7
        utot=0
        for i in range(-1,2):
            for j in range(-1,2):
                if (i!=0) or (j!=0):
                    flag=this|(pixcol((x+width+i)%width,(y+height+j)%height))&15
                    utot=utot+util[flag]
        pixset(x,y,utot*0x100+(pixcol(x,y)&15)) # Utility x 256; final nybble gives type

    # Function to pick the next occupant of (x,y)
    def pickbest(x,y):
        bestsofar=pixcol(x,y)
        if randrange(5)>0: # With probability of 20%, retain current occupant
            for i in range(-1,2):
                for j in range(-1,2): # Otherwise, find best in neighbourhood
                    if (pixcol((x+width+i)%width,(y+height+j)%height)&0xFFFF00)>(bestsofar&0xFFFF00):
                        bestsofar=pixcol((x+width+i)%width,(y+height+j)%height)
        pixset(x,y,pixcol(x,y)+(bestsofar&15)*16) # penultimate nybble was clear

    # Function to fix next generation colour, based on penultimate nybble
    def fixbest(x,y):
        if (pixcol(x,y)&16)>0:  # if 16 bit is set, red
            pixset(x,y,0xFF0001)
        elif(pixcol(x,y)&32)>0: # if 32 bit is set, green
            pixset(x,y,0x00FF02)
        else:
            pixset(x,y,0x0000FC)  # otherwise, blue

    # Main program, starts by setting Canvas
    canvas(0,0,width,height)

    # Set original map, with 2% blue, 14% green and 84% red
    noupdate()
    for i in range(width):
        for j in range(height):
            if randrange(50)==0:
                pixset(i,j,0x0000FC)
            elif randrange(7)==0:
                pixset(i,j,0x00FF02)
            else:
                pixset(i,j,0xFF0001)
    update()

    # Pause to show original map
    pause(1000)

    # Repeatedly update generations until Escape is pressed
    while get_key_sym()!="Escape":
        noupdate()
        for i in range(width):
            for j in range(height):
                utility(i,j)
        for i in range(width):
            for j in range(height):
                pickbest(i,j)
        for i in range(width):
            for j in range(height):
                fixbest(i,j)
        update()