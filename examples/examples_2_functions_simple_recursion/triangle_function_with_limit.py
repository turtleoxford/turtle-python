import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    colour(black)
    # draws a triangle of the specified size,
    # but only if that size is greater than 1
    def triangle(size: int):
        if (size>1):
            forward(size)
            right(120)
            forward(size)
            right(120)
            forward(size)
            right(120)

    # move to start, without drawing
    penup()
    movexy(-100,150)
    pendown()
    # draw a triangle of size 256
    triangle(256)