import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    facesize=100
    spongesize=40

    def face(size):

        def eye():
            colour(white)
            ellblot(size*3/20,size/10)
            colour(emerald)
            blot(size*9/100)
            colour(black)
            blot(size/25)

        direction(0)
        colour(peach)
        blot(size)
        colour(darkred)
        blot(size*7/10)
        forward(size*3/20)
        colour(peach)
        blot(size*3/4)
        back(size*3/10)
        colour(royal)
        blot(size*3/20)
        penup()
        forward(size*9/20)
        left(90)
        forward(size*2/5)
        eye()
        back(size*4/5)
        eye()

    x=300
    y=700
    xvel=8
    yvel=-4
    while 0<1:
        noupdate()
        colour(white)
        setxy(x,y)
        blot(facesize+spongesize)
        x=x+xvel
        y=y+yvel
        setxy(x,y)
        face(facesize)
        update()
        pause(10)
        if (status("mouse1")>0) and (hypot(get_clickx()-x,get_clicky()-y)<facesize):
            setxy(get_clickx(),get_clicky())
            colour(randcol(4))
            blot(spongesize)
            pause(100)
        if (x<facesize) or (x>999-facesize):
            xvel=-xvel
        if (y<facesize) or (y>999-facesize):
            yvel=-yvel