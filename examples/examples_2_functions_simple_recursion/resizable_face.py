import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # draws a face of the given radius
    def face(radius):
        # draws an eye of appropriate size
        def eye():
            colour(white)
            ellblot(radius*3/20,radius/10)
            colour(emerald)
            blot(radius*9/100)
            colour(black)
            blot(radius/25)

        # avoid drawing lines as Turtle moves
        penup()
        # draw head with blot of given radius
        colour(peach)
        blot(radius)
        # draw mouth using overlapping blots
        colour(darkred)
        blot(radius*7/10)
        forward(radius*3/20)
        colour(peach)
        blot(radius*3/4)
        # draw blue nose
        back(radius*3/10)
        colour(royal)
        blot(radius*3/20)
        # move to left eye position
        forward(radius*9/20)
        left(90)
        # Turtle is now pointing leftwards
        forward(radius*2/5)
        # draw left eye
        eye()
        # move to right eye position
        back(radius*4/5)
        # draw right eye
        eye()

    # draw a face of radius 200
    face(200)