import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # draws a star with given points & colour
    def star(points,colr):
        # set the size of a "degree" so there
        # are twice as many in a complete circle
        # as there are points in the polygon
        angles(points*2)
        for count in range(points):
            # move out to point
            forward(450)
            # move back to centre
            back(450)
            # forget visit back to centre
            forget(1)
            # turn right by 1 "degree", i.e.
            # halfway round to the next point
            right(1)
            # move out to inner corner
            forward(200)
            # move back to centre
            back(200)
            # forget visit back to centre
            forget(1)
            # turn right by 1 "degree", i.e. the
            # rest of the way to the next point
            right(1)
        # set specified colour
        colour(colr)
        # draw polygon joining remembered points
        polygon(points*2)

    # do not draw as Turtle moves
    penup()
    # draw stars with increasing points
    for n in range(3,13):
        # each star is a different colour
        star(n,rgb(n-2))
        # pause to enable each to be seen
        pause(500)