import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    xleft=1
    xright=1000
    ytop=1
    ybottom=1000
    gridscale=5
    gridthick=64

    def background():
        thickness(gridthick)
        colour(darkgrey)
        for x in range(1,gridscale):
            setxy(xleft+divmult(xright-xleft,gridscale,x),ytop)
            drawxy(0,ybottom-ytop)
        for y in range(1,gridscale):
            setxy(xleft+gridthick/2,ytop+divmult(ybottom-ytop,gridscale,y))
            drawxy(xright-xleft-gridthick,0)
        colour("black")
        setxy(xleft,ytop)
        drawxy(xright-xleft,0)
        drawxy(0,ybottom-ytop)
        drawxy(xleft-xright,0)
        drawxy(0,ytop-ybottom)
        for x in range(gridscale):
            for y in range(gridscale):
                cx=xleft+divmult(xright-xleft,gridscale,x)+gridthick
                cy=ytop+divmult(ybottom-ytop,gridscale,y)+gridthick
                r=divmult(255,gridscale-1,x)
                g=divmult(255,gridscale-1,y)
                b=divmult(255,2*gridscale-2,2*gridscale-2-x-y)
                cell_width=divmult(xright-xleft,gridscale,1) - gridthick
                cell_height=divmult(ybottom-ytop,gridscale,1) - gridthick
                recolour(cx - 0.5 * gridthick,cy - 0.5 * gridthick,cx+cell_width,cy+cell_height,(r*0x10000)+(g*0x100)+b)

    canvas(xleft,ytop,xright-xleft+1,ybottom-ytop+1)
    background()