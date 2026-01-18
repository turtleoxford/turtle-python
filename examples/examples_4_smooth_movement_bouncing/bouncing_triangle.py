import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    size = 100

    x=300
    y=700
    d=0

    # draws a triangle, and checks whether it meets the edge of the canvas
    def triangle(col):
        global xEdge,yEdge
        xEdge=False
        yEdge=False
        setxy(x,y)
        direction(d)
        colour(col)
        for count in range(3):
            forward(size)
            if abs(t._x-500)>495:
                xEdge=True
            if abs(t._y-500)>495:
                yEdge=True
            back(size)
            forget(1)
            right(120)
        polygon(3)

    # set starting velocity
    xVelocity=8
    yVelocity=-4
    dVelocity=5
    while 0<1:
        noupdate()
        # rub out existing triangle
        blank(white)
        # move to next location
        x=x+xVelocity
        y=y+yVelocity
        d=(d+dVelocity)%360
        # draw new triangle
        triangle(red)
        update()
        pause(10)
        # "bounce" (i.e. invert velocity) at canvas edges
        if xEdge:
            xVelocity=-xVelocity
            dVelocity=-dVelocity
        if yEdge:
            yVelocity=-yVelocity
            dVelocity=-dVelocity