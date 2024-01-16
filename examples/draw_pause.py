#!/bin/python3
from turtle_oxford import *

with turtle_canvas(0, 0, 1000, 1000) as t:
    # draw green blot radius 100, then pause
    colour("green")
    blot(100)
    pause(1000)
    # draw red line length 450 upwards, then pause
    colour("red")
    forward(450)
    pause(1000)
    # turn right 90 degrees and change thickness
    right(90)
    thickness(9)
    # change colour, pause, draw line length 300
    colour("blue")
    pause(1000)
    forward(300)
