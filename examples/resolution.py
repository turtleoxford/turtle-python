from turtle_oxford import *

width = 100
height = 100
with turtle_canvas(0, 0, 1000, 1000):
    resolution(width, height)
    pixset(1, 1, "black")
    for i in range(0, width):
        for j in range(0, height):
            if i == 1 and j == 1:
                assert pixcol(i, j) == 0x000000
            else:
                assert pixcol(i, j) == 0xFFFFFF
