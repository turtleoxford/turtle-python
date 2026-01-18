import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    # RDRAW draws a single stem with two recursive
    # calls, one at DIST units (and pointing 30
    # degrees left), the other a further DIST/3
    # units (and pointing 20 degrees right).
    # It then retraces to its starting point.
    def rdraw(dist,level):
        thickness(level*2) # Thicker at higher levels
        forward(dist) # Move forward by DIST
        left(30)      # Point left by 30 degrees
        if level>0:   # Recursive call 1 (if level>0)
            rdraw(3*dist/4,level-1)
        right(30)     # Straighten up
        thickness(level*2) # Restore thickness
        forward(dist/3) # Forward another DIST/3
        right(20)     # Point right by 20 degrees
        if level>0:   # Recursive call 2 (if level>0)
            rdraw(3*dist/4,level-1)
        left(20)      # Straighten up
        back(dist/3)  # Retrace DIST/3
        back(dist)    # Retrace DIST back to start

    # The main program simply sets the scene and
    # then calls RDRAW, starting at level 10
    blank(black)    # Blacken the Canvas
    penup()
    movexy(0,400)   # Move down to starting point
    pendown()
    colour(emerald) # Draw tree in emerald
    rdraw(180,10)