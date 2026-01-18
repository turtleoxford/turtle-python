import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # set starting point and velocity
    setxy(100,700)
    xVelocity=8
    yVelocity=-4
    while True:
        noupdate()
        # rub out existing ball
        colour(white)
        blot(53)
        # move to next location
        movexy(xVelocity, yVelocity)
        # draw new ball
        colour(red)
        blot(50)
        update()
        pause(10)
        # "bounce" (i.e. invert velocity) at canvas edges
        if (t._x<50) or (t._x>950):
            xVelocity=-xVelocity
        if (t._y<50) or (t._y>950):
            yVelocity=-yVelocity