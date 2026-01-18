import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # black out canvas
    blank(black)
    # initialise variables
    colourInc=randint(0,4)
    colourCode=randint(1,20)
    lineLength=0
    thickness(16)
    # draw a multi-coloured spiral by repeating the
    # following until the move forward distance > 250
    while not(lineLength>250):
        # cycle through some standard Turtle colours
        colourCode=(colourCode+colourInc)%20+1
        colour(rgb(colourCode))
        # move forward by an increasing amount
        lineLength=lineLength+1
        forward(lineLength)
        # turn right by 30 degrees
        right(30)