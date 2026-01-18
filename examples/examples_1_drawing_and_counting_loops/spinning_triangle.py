import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    colour("black")
    # counting from 0 to 299 in steps of 1 ...
    for i in range(300):
    # short form of "for i in range(0,300,1)"
        # move forward by 3 times the count number
        forward(i*3)
        # turn right by 121 degrees
        right(121)