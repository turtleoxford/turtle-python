import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    thickness(4)
    penup()
    # counting from 0 to 29 ...
    for blotCount in range(30):
        # set direction, multiple of 36 degrees
        direction(blotCount*36)
        # move 260 units from middle of canvas
        forward(260)
        # draw large black and smaller white blot
        colour(black)
        blot(150)
        colour(white)
        blot(56)
        # set standard Turtle colour blotCount+1
        colour(rgb(blotCount+1))
        # draw 19 circles, radius 56 to 200 step 8
        for circleCount in range(56,201,8):
            circle(circleCount)
    # reposition Turtle to canvas middle
        back(260)
    # pause for 1/5 second before continuing
        pause(200)