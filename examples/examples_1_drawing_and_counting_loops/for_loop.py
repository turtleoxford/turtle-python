import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    # counting from 1 to 200 ...
    canvas(0, 0, 1000, 1000)
    for count in range(1, 201):
        # move forward and turn right 5 degrees
        forward(count / 3)
        right(5)
        # draw red blot radius 200
        colour("red")
        blot(200)
        # draw black circle around the red blot
        colour("black")
        circle(200)
