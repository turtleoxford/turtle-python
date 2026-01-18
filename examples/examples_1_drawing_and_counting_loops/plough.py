import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # set canvas to black, and pen to lightblue
    blank(black)
    colour(lightblue)
    # place Turtle and draw blots for stars
    setxy(100,200)
    blot(10)
    setxy(300,250)
    blot(10)
    setxy(420,350)
    blot(10)
    setxy(570,490)
    blot(10)
    setxy(900,560)
    blot(10)
    setxy(840,720)
    blot(10)
    setxy(590,660)
    blot(10)
    setxy(570,490)
    # join dots to highlight plough shape
    colour(silver)
    polyline(8)