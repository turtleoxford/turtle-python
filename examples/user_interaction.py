#!/bin/python3
from turtle_oxford import *

with turtle_canvas() as t:
    canvas(0, 0, 3, 3)
    update()
    for i in range(100):
        detect("click", 0)
        blank(cream)
        colour(black)
        setxy(0, 0)
        display(f"{get_clickx()}, {get_clicky()}", size=1)
