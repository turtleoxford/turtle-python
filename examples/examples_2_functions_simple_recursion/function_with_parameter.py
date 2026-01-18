import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # draws a prong of the given size
    def prong(size):
        forward(size)
        # blot radius is 1/20 of prong length
        blot(size/20)
        back(size)

    # draw 360 prongs of decreasing size
    for count in range(360,0,-1):
        colour(randcol(10))
        # longest is 460, shortest is 101
        prong(count+100)
        # 61 degrees gives six-arm spiral
        right(61)