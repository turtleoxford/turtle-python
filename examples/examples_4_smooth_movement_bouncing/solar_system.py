import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    sunRadius=50000
    planets=8
    radius=[2433,6053,6371,3380,71492,58219,23470,23716]
    distanceFromSun=[5795,10811,14957,22784,77814,142700,287030,449990]
    speed=[1607,1174,1000,802,434,323,182,159]
    colr=[white,ochre,blue,orangered,lightred,cream,cyan,royal]
    rotation=[0]*planets

    # multiply canvas dimensions by 1000
    angles(360000)
    canvas(0,0,1000000,1000000)
    penup()
    while True:
        noupdate()
        # rub out previous frame
        blank(black)
        # draw sun
        home()
        colour(yellow)
        blot(sunRadius)
        # draw each planet
        for i in range(planets):
            home()
            # draw a white circle for the orbit
            colour(white)
            circle(distanceFromSun[i]+sunRadius)
            # reset to home so angle math is consistent per planet
            home()
            # move to next position and draw the planet
            direction(-rotation[i])
            forward(distanceFromSun[i]+sunRadius)
            rotation[i]=(rotation[i]+speed[i])
            colour(colr[i])
            if i<=3:
                blot(radius[i]*2) # make inner planets double scale
            else:
                blot(radius[i]/2) # make outer planets half scale
        update()