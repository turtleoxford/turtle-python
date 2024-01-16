#!/bin/python3
from turtle_oxford import *
from random import randint

width = 32
height = 32
with turtle_canvas(0, 0, 900, 900) as t:
    resolution(width, height)
    for x in range(width):
        for y in range(height):
            if randint(0, 6) == 0:
                pixset(x, y, 0xFFFFFD)
    while get_key_sym() != "Escape":
        noupdate()
        for x in range(width):
            for y in range(height):
                dn = 0
                for i in range(-1, 2, 1):
                    for j in range(-1, 2, 1):
                        dn += (
                            pixcol((x + i + width) % width, (y + j + height) % height)
                            & 1
                        )
                if ((pixcol(x, y) & 1 == 0) and (dn < 5 or dn > 6)) or (
                    (pixcol(x, y) & 1 == 1) and (dn == 6)
                ):
                    pixset(x, y, pixcol(x, y) ^ 2)
        for x in range(width):
            for y in range(height):
                if (pixcol(x, y) & 3) % 3 != 0:
                    pixset(x, y, pixcol(x, y) ^ 0xFFFFFD)
            update()
