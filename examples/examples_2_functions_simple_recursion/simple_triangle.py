import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    colour(black)
    # move to start, without drawing
    penup()
    movexy(-100,150)
    pendown()
    # draw first side, and turn
    forward(256)
    right(120)
    # draw second side, and turn
    forward(256)
    right(120)
    # draw third side, and turn
    forward(256)
    right(120)