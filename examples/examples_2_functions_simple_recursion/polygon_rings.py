import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # draws an annulus (ring) with given inner
    # radius, width, and coloured segment angle
    def annulus(inner: int,width: int,angle: int):
        # count enough segments to go full circle
        for count in range(round(360/angle)+1):
            # move from centre to outside edge
            forward(inner+width)
            # move back to inside edge
            back(width)
            # move back to centre
            back(inner)
            # forget visit to centre
            forget(1)
            # turn right by specified angle
            right(angle)
            # move from centre to inside edge
            forward(inner)
            # move to outside edge
            forward(width)
            # rotate around 20 standard colours
            colour(rgb(count%20+1))
            # draw coloured quadrilateral
            polygon(4)
            # move back to centre
            back(inner+width)

    penup()
    # draw black blot for background
    blot(500)
    # draw five annuli within the blot
    annulus(410,80,2)
    annulus(310,80,3)
    annulus(210,80,5)
    annulus(110,80,7)
    annulus(10,80,1)