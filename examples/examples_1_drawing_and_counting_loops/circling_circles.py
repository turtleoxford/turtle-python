import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # set up Turtle
    movexy(0, 0)
    thickness(6)
    penup()
    blank(black)
    colour(orange)
    # counting from 0 to 35 ...
    for count in range(36):
        # move 200 units from middle of canvas
        forward(200)
        # draw circle radius 200 centred there
        circle(200)
        # move back to middle of canvas
        back(200)
        # turn right 10 degrees - 1/36 of full turn
        right(10)
        # pause 25 milliseconds before next circle
        pause(25)