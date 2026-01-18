import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    faceRadius = 100

    # draws a face of the given radius
    # N.B. copied from the Resizable face example
    def face(radius):
        # draws an eye sized relative to the face
        def eye():
            colour(white)
            ellblot(radius*3/20,radius/10)
            colour(emerald)
            blot(radius*9/100)
            colour(black)
            blot(radius/25)

        direction(0)
        # draw head
        colour(peach)
        blot(radius)
        # draw mouth
        colour(darkred)
        blot(radius*7/10)
        forward(radius*3/20)
        colour(peach)
        blot(radius*3/4)
        # draw nose
        back(radius*3/10)
        colour(royal)
        blot(radius*3/20)
        # move to left eye position (without drawing)
        penup()
        forward(radius*9/20)
        left(90)
        forward(radius*2/5)
        # draw left eye
        eye()
        # move to right eye position (without drawing)
        back(radius*4/5)
        # draw right eye
        eye()

    # set starting point and velocity
    x=300
    y=700
    xVelocity=8
    yVelocity=-4
    while 0<1:
        noupdate()
        # rub out existing face
        colour(white)
        blot(faceRadius+2)
        # move to next location
        x=x+xVelocity
        y=y+yVelocity
        setxy(x,y)
        # draw new face
        face(faceRadius)
        # reset x and y after face drawing
        setxy(x,y)
        update()
        pause(10)
        # "bounce" (i.e. invert velocity) at canvas edges
        if (x<faceRadius) or (x>999-faceRadius):
            xVelocity=-xVelocity
        if (y<faceRadius) or (y>999-faceRadius):
            yVelocity=-yVelocity