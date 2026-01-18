import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    width=100
    height=100
    cellcol=[0xFFFFFE,0x000001]
    nextstate=[0]*8

    def setup(rulecode):
        for nhood in range(8):
            nextstate[nhood]=rulecode%2
            rulecode=rulecode//2

    def nextgen(g):
        n1=0
        n2=0
        for x in range(-1,width+1):
            xmod=(x+width)%width
            thispix=pixcol(xmod,g-1)&1
            n3=n2*2+thispix
            n2=n1*2+thispix
            n1=thispix
            if x>0:
                pixset(x-1,g,cellcol[nextstate[n3]])

    canvas(0,0,width,height)
    for n in range(4,46):
        rule=n*4+2
        setup(rule)
        noupdate()
        blank(white)
        for x in range(width):
            pixset(x,0,cellcol[randrange(2)])
        for generation in range(1,height):
            nextgen(generation)
        setxy(0,height-15)
        box(25+len(str(rule))*7,14,cream,False)
        colour(black)
        display('Rule '+str(rule),4,8)
        update()
        pause(500)