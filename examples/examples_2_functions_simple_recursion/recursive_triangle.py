import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    colour(black)
    # draws triangles recursively, starting with
    # one of the given size, but then also making
    # half-sized triangles at each triangle point
    def triangle(size):
        if (size>1):
            forward(size)
            triangle(size/2)
            right(120)
            forward(size)
            triangle(size/2)
            right(120)
            forward(size)
            triangle(size/2)
            right(120)

    # move to start, without drawing
    penup()
    movexy(-100,150)
    pendown()
    # draw a recursive triangle of size 256
    triangle(256)