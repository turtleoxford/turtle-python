import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    # KDRAW recursively draws a Koch curve
    def kdraw(dist,level):
        if level==0:
            forward(dist) # if level 0, just move
        else:             # forward; otherwise ...
            kdraw(dist/3,level-1) # forward dist/3
            left(60)
            kdraw(dist/3,level-1) # replace the
            right(120)            # middle third
            kdraw(dist/3,level-1) # with a point
            left(60)
            kdraw(dist/3,level-1) # forward dist/3

    # The main program draws three Koch curves
    # so as to make a complete circuit
    blank(black)              # blacken Canvas
    penup()
    movexy(0,430)             # start at (500,930)
    pendown()
    left(30)                  # set initial angle
    for count in range(3):    # FOR 0, 1, 2 ...
        colour(rgb(count+21)) # choose colour
        kdraw(729,4)          # draw level-4 curve
        right(120)            # turn 120 degrees