import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    snakecolour = purple
    applecolour = green
    boardsize =30

    snakelength=2
    crash=False

    def newapple():
        x=randint(0, boardsize-1)
        y=randint(0, boardsize-1)
        while pixcol(x,y)==snakecolour:
            x=randint(0, boardsize-1)
            y=randint(0, boardsize-1)
        pixset(x,y,applecolour)

    canvas(0,0,boardsize,boardsize)
    
    angles(4)
    blank(lightblue)
    colour(snakecolour)
    thickness(1)
    penup()
    forward(1)
    newapple()
    while not crash:
        noupdate()
        key = get_key_sym()
        if (key == "Up") and (t._direction!=2):
            direction(0)
        elif (key == "Right") and (t._direction!=3):
            direction(1)
        elif (key == "Down") and (t._direction!=0):
            direction(2)
        elif (key == "Left") and (t._direction!=1):
            direction(3)
        
        forward(1)
        
        if (t._x<0) or (t._x>=boardsize) or (t._y<0) or (t._y>=boardsize):
            crash=True
        elif pixcol(t._x,t._y)==snakecolour:
            crash=True
        elif pixcol(t._x,t._y)==applecolour:
            snakelength=snakelength+1
            pixset(t._x,t._y,snakecolour)
            newapple()
            
        colour(lightblue)
        polyline(snakelength+2)
        colour(snakecolour)
        polyline(snakelength)
        update()
        pause(250-(snakelength*3))
        
    # resolution(1000,1000)
    blank(lilac)
    setxy(boardsize//4,2*boardsize//5)
    display('Score '+str(snakelength-2),"Arial",100)