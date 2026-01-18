import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # draws a single "prong" and then returns
    def prong():
        forward(400)
        blot(20)
        back(400)

    # repeatedly draw prongs in random colours
    # until Turtle is pointing north again
    right(61)
    while t._direction != 0:
        colour(randcol(10))
        prong()
        # right turn gives impression of motion
        right(61)