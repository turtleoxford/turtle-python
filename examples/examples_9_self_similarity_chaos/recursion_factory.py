import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    penup()
    numsides=6   # number of sides in each polygon
    initsize=240 # initial length of polygon side
    shrink=40    # shrink n/120ths each recursion
    rangle=180   # recursion angle from centre line
    polygap=0    # polygon gap, n/120ths at RANGLE
    levels=5     # how many levels of recursion
    slowdraw=3   # levels to be shown slow-drawing
    mode=1       # 1=lines ; 2=blots ; 3=circles
    firstcol=5   # colour of first level polygon
    colinc=4     # increment for successive colours
    minthick=2   # minimum line thickness
    addthick=6   # extra thickness per level x 12
    circsize=60  # radius n/120ths of polygon side

    # PROCEDURE RECURSE is the program's heart. SIZE gives the
    # polygon side at the current level; DEPTH the levels of
    # recursion to go; COL the colour; FLAG is explained below.
    # Note that when RECURSE is called, the turtle is always at
    # a corner, facing towards the centre of the polygon at the
    # current level. So after turning HALFANGLE to the left, it
    # will be facing along the left-hand edge of the polygon.

    def recurse(flag,size,depth,col):
        if depth>0:         # Recursion stops when DEPTH=0.
            if depth<slowlev: # When DEPTH is less than SLOWLEV, no
                noupdate()      # screen updating makes it faster
            else:
                update()
            if flag==1:                        # FLAG=1 for first
                for flag in range(2,4):          # call at each level.
                    storex=turtx()
                    storey=turty()                 # RECURSE calls itself
                    for sides in range(numsides):  # NUMSIDES times with
                        recurse(flag,size,depth,col) # FLAG=2, then FLAG=3
                    t._x = storex
                    t._y = storey  # Then the start position is restored
            else:
                penup()                       # FLAG=2 draws one side
                if flag==2:                   # of the polygon at the
                    colour(rgb(col))            # current level.
                    thickness(minthick+((depth-1)*addthick)/12)
                    if mode==1:
                        pendown()                 # MODE=1: draw lines
                    elif mode==2:
                        blot(size*circsize/120)   # MODE=2: draw blots
                    else:
                        circle(size*circsize/120) # MODE=3: draw circles
                left(halfangle)
                forward(size)
                right(180-halfangle+rangle)   # FLAG=3 follows the
                if flag==3:                   # same path, recursively
                    forward(size*polygap/120)   # calling the next level
                    recurse(1,(size*shrink)/120,depth-1,((col+colinc-1)%7)+1)
                    back(size*polygap/120)
                left(rangle)

    # The main program first checks that NUMSIDES divides exactly
    # into 180 (since otherwise the result is a mess), and if so ...
    if 180%numsides==0:
        blank(black)                  # Blacken the Canvas.
        halfangle=90-(180/numsides)   # Calculate HALFANGLE and
        slowlev=levels+1-slowdraw     # SLOWLEV, while ensuring
        if slowlev>levels-1:          # that at least two levels
            slowlev=levels-1            # are slow-drawn.
        movexy(0,initsize)            # Centralise the pattern,
        recurse(1,initsize,levels,firstcol) # and off we go!