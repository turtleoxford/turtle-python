import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    # Set how many levels to draw: a setting of
    # 2 gives a simple Koch curve in the centre 
    maxlevel=5

    # KDRAW recursively draw a Koch curve
    def kdraw(dist,level):
        if level==0:
            forward(dist) # if level 0, just move
        else:           # forward; otherwise ...
            kdraw(dist/3,level-1) # forward dist/3
            left(90)
            kdraw(dist/3,level-1) # replace the
            right(90)             # middle third
            kdraw(dist/3,level-1) # with a square
            right(90)             # diversion
            kdraw(dist/3,level-1)
            left(90)
            kdraw(dist/3,level-1) # forward dist/3

    # The main program draws four Koch curves
    # so as to make a complete circuit, then
    # does the same at a smaller scale
    blank(black)              # blacken Canvas
    penup()
    movexy(0,486)             # start at (500,986)
    pendown()
    left(45)                  # set initial angle
    for count in range(4):    # FOR 0, 1, 2, 3 ...
        colour(rgb(count+21))  # choose colour
        kdraw(729,maxlevel)    # draw level-5 curve
        right(90)              # turn 90 degrees
    # Now do smaller circuit
    movexy(0,-323)            # start at (500,663)
    for count in range(4):    # FOR 0, 1, 2, 3 ...
        colour(rgb(count+21))  # choose colour
        kdraw(243,maxlevel-1)  # draw level-4 curve
        right(90)              # turn 90 degrees