import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # set starting point
    x=100
    y=700
    for count in range(100):
        noupdate()
        # rub out previous ball
        colour(white)
        blot(53)
        # move to next point
        x=x+8
        y=y-4
        setxy(x,y)
        # draw new ball
        colour(red)
        blot(50)
        update()
        pause(10)