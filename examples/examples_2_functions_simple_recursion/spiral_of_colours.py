import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # draws a line and turns right 60 degrees
    def lineTurn():
        forward(lineLength)
        right(60)

    # make canvas black
    blank(black)
    # position Turtle so pattern fits neatly
    forward(15)
    # set line thickness and initial length
    thickness(27)
    lineLength=20
    # repeatedly, until lineLength gets to 510
    while lineLength<510:
        # choose one of the first 40 Turtle colours
        colour(randcol(40))
        # call lineTurn function, then pause
        lineTurn()
        pause(50)
        # increment lineLength value
        lineLength=lineLength+10