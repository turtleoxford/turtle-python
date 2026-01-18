import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # set starting point and velocity
    x=100
    y=700
    xVelocity=8
    yVelocity=-4
    while True:
        noupdate()
        # rub out existing ball
        colour(white)
        blot(52)
        # move to next location
        x=x+xVelocity
        y=y+yVelocity
        setxy(x,y)
        # draw new ball
        colour(red)
        blot(50)
        update()
        pause(10)
        # "bounce" (i.e. invert velocity) at canvas edges
        if (x<50) or (x>949):
            xVelocity=-xVelocity
        if (y<50) or (y>949):
            yVelocity=-yVelocity