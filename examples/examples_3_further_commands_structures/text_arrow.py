import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # draw red blot
    colour(red)
    blot(20)
    # print violet text, font style 4, size 36
    colour(violet)
    display('You are here',4,36)
    # draw blue multi-part "curve"
    setxy(790,540)
    colour(blue)
    drawxy(40,0)
    drawxy(28,-28)
    drawxy(0,-40)
    drawxy(-28,-28)
    drawxy(-40,0)
    # position Turtle in centre of blot
    setxy(500,500)
    # draw line connecting two last points
    polyline(2)
    # visit other points of triangle head
    setxy(530,480)
    setxy(535,505)
    # fill triangle of last three points
    polygon(3)
    # for neatness, end up in centre
    setxy(500,500)