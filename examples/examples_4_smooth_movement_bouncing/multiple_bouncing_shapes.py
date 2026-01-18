import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    minSize=70
    maxSize=130
    shapes=6
    x=[0]*shapes
    y=[0]*shapes
    d=[0]*shapes
    xVelocity=[0]*shapes
    yVelocity=[0]*shapes
    dVelocity=[0]*shapes
    sides=[0]*shapes
    size=[0]*shapes
    colr=[0]*shapes

    # draws a polygon, and checks whether it meets the edge of the canvas
    def drawShape(sides,size,colr):
        global xEdge,yEdge
        xEdge=False
        yEdge=False
        colour(colr)
        for count in range(sides):
            forward(size)
            if abs(t._x-500)>495:
                xEdge=True
            if abs(t._y-500)>495:
                yEdge=True
            back(size)
            forget(1)
            right(360/sides)
        polygon(sides)

    # set initial properties for each shape
    for n in range(shapes):
        sides[n]=n+3
        size[n]=randint(minSize,maxSize)
        colr[n]=rgb(n+1)
        x[n]=randint(size[n],1000-size[n])
        y[n]=randint(size[n],1000-size[n])
        d[n]=randrange(360)
        xVelocity[n]=randint(-7,7)
        yVelocity[n]=randint(-7,7)
        dVelocity[n]=randint(3,6)
    while 0<1:
        noupdate()
        # rub out previous shapes
        blank(white)
        # draw each shape in its next position
        for n in range(shapes):
            # move to next position
            x[n]=x[n]+xVelocity[n]
            y[n]=y[n]+yVelocity[n]
            d[n]=(d[n]+dVelocity[n])%360
            setxy(x[n],y[n])
            direction(d[n])
            # draw shape
            drawShape(sides[n],size[n],colr[n])
            # "bounce" (i.e. invert velocity) at canvas edges
            if xEdge:
                xVelocity[n]=-xVelocity[n]
                dVelocity[n]=-dVelocity[n]
            if yEdge:
                yVelocity[n]=-yVelocity[n]
                dVelocity[n]=-dVelocity[n]
        update()
        pause(5)