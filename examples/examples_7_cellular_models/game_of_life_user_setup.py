import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    width=32
    height=32
    canvas(0,0,width,height)
    while True:
        mk = detect("mousekey", 0)
        if mk == "mouse1":
            pixset(get_clickx(), get_clicky(), black)
        elif mk == "mouse3":
            pixset(get_clickx(), get_clicky(), white)
        else:
            break
    while get_key_sym() != "Escape":
        noupdate()
        for x in range(width):
            for y in range(height):
                dn=0
                for i in range(-1,2):
                    for j in range(-1,2):
                        dn += pixcol((x + i) % width, (y + j) % height) & 1
                if ((pixcol(x,y)&1==0) and ((dn<5) or (dn>6))) or ((pixcol(x,y)&1==1) and (dn==6)):
                    pixset(x,y,pixcol(x,y)^2)
        for x in range(width):
            for y in range(height):
                if (pixcol(x, y) & 3) % 3 != 0:
                    pixset(x, y, pixcol(x, y) ^ 0xFFFFFD)
        update()