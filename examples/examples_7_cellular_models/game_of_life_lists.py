import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    width=32
    height=32
    canvas(0,0,width,height)

    # create two-dimensional THISGEN list
    thisgen=[]
    for x in range(width):
        xlist=[]
        for y in range(height):
            # every element is 0
            xlist.append(0)
        thisgen.append(xlist)

    # create two-dimensional NEXTGEN list
    nextgen=[]
    for x in range(width):
        xlist=[]
        for y in range(height):
            # each element has 1/7 chance of 1
            xlist.append(randrange(7)==0)
        nextgen.append(xlist)

    # as long as ESCAPE key isn't pressed ...
    while get_key_sym() != "Escape":
        noupdate()
        for x in range(width):
            for y in range(height):
                # copy NEXTGEN into THISGEN
                thisgen[x][y]=nextgen[x][y]
                # display THISGEN pattern
                if thisgen[x][y]:
                    pixset(x,y,maroon)
                else:
                    pixset(x,y,lightgreen)
        # update Canvas with new pattern
        update()

        # for each cell [x][x] in THISGEN list ...
        for x in range(width):
            for y in range(height):
                livenb=0
                # count live cells in its neighbourhood
                for i in range(-1,2):
                    for j in range(-1,2):
                        if thisgen[(x+i)%width][(y+j)%height]:
                            livenb+=1
                # apply LIFE rules to calculate NEXTGEN value
                if thisgen[x][y]:
                    nextgen[x][y]=((livenb==3) or (livenb==4))
                else:
                    nextgen[x][y]=(livenb==3)