import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # set ring radius and thickness
    ringRadius=130
    thickness(20)
    # raise pen to avoid drawing lines
    penup()
    # draw black ring
    colour(black)
    forward(50)
    circle(ringRadius)
    # draw blue ring
    left(90)
    forward(300)
    colour(blue)
    circle(ringRadius)
    # draw red ring
    back(600)
    colour(red)
    circle(ringRadius)
    # draw green ring
    forward(150)
    right(90)
    back(125)
    colour(lime)
    circle(ringRadius)
    # draw yellow ring
    left(90)
    forward(300)
    colour(yellow)
    circle(ringRadius)