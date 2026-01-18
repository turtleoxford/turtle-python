import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # draw a 3d-style coloured ball
    def ball3d(colr,step):
        # start with specified colour code
        colour(colr)
        # draw 40 progressively smaller blots
        for count in range(40,0,-1):
            blot(count*6)
            # moving their centre by 3 each time
            forward(3)
            # and making the colour lighter
            current_colour_int = int(t._colour[1:], 16)
            new_colour_int = current_colour_int + int(step)
            if new_colour_int > 0xFFFFFF:
                new_colour_int = 0xFFFFFF
            colour(new_colour_int)

    # turn so brightest point is up and right
    right(60)
    # draw a cyan ball at top left
    setxy(250,250)
    ball3d(0x00FFFF,0x50000)
    # draw a chocolate brown ball at top right
    setxy(750,250)
    ball3d(0xD2691E,0x10102)
    # draw a dark red ball at bottom left
    setxy(250,750)
    ball3d(0xA90000,0x20202)
    # draw a yellow ball at bottom right
    setxy(750,750)
    ball3d(0xFFD800,0x101)