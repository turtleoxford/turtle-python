import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # draws a polygon with given sides & colour
    def poly(sides,colr):
        # point Turtle horizontally to right
        direction(90)
        # trace shape with the Turtle
        for count in range(sides):
            # edge is shorter as sides increases
            forward(600/sides)
            # turn left by correct external angle
            left(360/sides)
        # fill with given colour
        colour(colr)
        polygon(sides)
        # draw black outline
        colour(black)
        polyline(sides+1)

    # do not draw as Turtle moves
    penup()
    # thickness is used by POLYLINE command
    thickness(4)
    # place Turtle for first polygon
    setxy(250,400)
    # draw blue triangle
    poly(3,blue)
    # place Turtle for second polygon
    setxy(550,400)
    # draw red square
    poly(4,red)
    setxy(850,400)
    # draw yellow pentagon
    poly(5,yellow)
    setxy(300,750)
    # draw pink hexagon
    poly(6,pink)
    setxy(590,750)
    # draw green heptagon
    poly(7,green)
    setxy(890,750)
    # draw turquoise octagon
    poly(8,turquoise)