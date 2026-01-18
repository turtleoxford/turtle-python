import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(800, 600) as t:
    width = 10
    height = 15
    # set up canvas coordinates and resolution
    canvas(1,1,width,height)
    # draw coloured pixels across bottom
    for x in range(1,width+1):
        pixset(x,height,rgb(x))
    # now enter interactive while loop
    # until ESCAPE key is pressed
    mk = ""
    current_colour = white
    while mk != "Escape":
        # detect mouse click or key within 5 seconds
        mk = detect("mousekey", 5000)
        if mk == "mouse1":
            # if left click, cell becomes turtle colour
            pixset(get_clickx(), get_clicky(), current_colour)
        elif mk == "mouse3":
            # if right click, turtle takes colour from cell
            current_colour = pixcol(get_clickx(), get_clicky())
            colour(current_colour)
        elif mk == "mouse2":
            # if middle click, cell takes random colour
            pixset(get_clickx(), get_clicky(), rgb(randint(1,10)))