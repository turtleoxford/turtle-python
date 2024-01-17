#!/bin/python3
from turtle_oxford import *

with turtle_canvas() as t:
    update()
    for i in range(100):
        det = detect("mousekey", 0)
        blank(cream)
        colour(black)
        display(det, size=36)
