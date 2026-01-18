import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    minSize=70
    maxSize=130
    balls=10
    x=[0]*balls
    y=[0]*balls
    xVelocity=[0]*balls
    yVelocity=[0]*balls
    size=[0]*balls
    colr=[0]*balls
    for n in range(balls):
        size[n]=randint(minSize,maxSize)
        colr[n]=rgb(n+1)
        x[n]=randint(size[n],1000-size[n])
        y[n]=randint(size[n],1000-size[n])
        xVelocity[n]=randint(-7,7)
        yVelocity[n]=randint(-7,7)
    while 1==1:
        noupdate()
        # rub out previous balls
        blank(white)
        # draw each ball in its next position
        for n in range(balls):
            # move to next position
            x[n]=x[n]+xVelocity[n]
            y[n]=y[n]+yVelocity[n]
            setxy(x[n],y[n])
            # draw ball
            colour(colr[n])
            blot(size[n])
            # "bounce" (i.e. invert velocity) at canvas edges
            if (x[n]<size[n]) or (x[n]>1000-size[n]):
                xVelocity[n]=-xVelocity[n]
            if (y[n]<size[n]) or (y[n]>1000-size[n]):
                yVelocity[n]=-yVelocity[n]
        update()
        pause(5)