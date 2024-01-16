from turtle_oxford import *
from random import randint

with turtle_canvas(0, 0, 1000, 1000) as t:
    # draws a star with given points & colour
    def star(points, colr):
        # set the size of a "degree" so there
        # are twice as many in a complete circle
        # as there are points in the polygon
        angles(points * 2)
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
        polygon(points * 2)

    # do not draw as Turtle moves
    penup()
    # draw stars with increasing points
    for n in range(3, 13):
        # each star is a different colour
        col = randint(0, 0xffffff)
        star(n, col)
        # pause to enable each to be seen
        pause(500)