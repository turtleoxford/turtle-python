import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # draw green blot radius 100, then pause
    colour("green")
    blot(100)
    pause(500)
    # draw red line length 450 upwards, then pause
    colour("red")
    forward(450)
    pause(500)
    # turn right 90 degrees and change thickness
    right(90)
    thickness(9)
    # change colour, pause, draw line length 300
    colour("blue")
    pause(500)
    forward(300)
