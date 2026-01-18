import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # draws circle or blot at Turtle position
    def drawit(doblot):
        if doblot:
            # draw a randomly coloured blot
            # without erasing any circle
            colour(randcol(10))
            blot(25)
        else:
            # erase any previous blot
            colour(black)
            blot(30)
            # draw randomly coloured circle
            colour(randcol(10))
            circle(25)

    # blacken the entire canvas
    blank(black)
    # set thickness for drawing circles
    thickness(10)
    # repeatedly draw circles or blots in a grid
    while True:
        # randint(1, 8) returns a value between 1 and 8
        # fix x coordinate from 111 to 888
        setx(randint(1,8)*111)
        # fix y coordinate from 111 to 888
        sety(randint(1,8)*111)
        # call drawit - randrange(2) returns 0 or 1:
        # 0 is the same as False; 1 is the same as True
        drawit(randrange(2))