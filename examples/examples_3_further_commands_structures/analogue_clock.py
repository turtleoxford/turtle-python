import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # draws hour and minute hands on a clock face
    def showhands(hours,minutes):
        # run out previous hands
        colour(white)
        blot(360)
        # draw hour hand and return to centre
        colour(red)
        direction(-hours*30)
        thickness(10)
        forward(250)
        back(250)
        # draw minute hand and return to centre
        direction(-minutes*6)
        thickness(6)
        forward(350)
        back(350)

    # draw black circle for clock face
    colour(black)
    thickness(10)
    circle(400)
    # initialise hours and minutes to zero
    hours=0
    minutes=0
    # repeatedly through the hours ...
    while hours<=12:
        # repeatedly through the minutes ...
        while minutes<=60:
            # draw both hands in the appropriate place
            showhands(hours,minutes)
            # pause 1/10 second [so clock goes 600 times too fast]
            pause(100)
            # count through minutes until it reaches 60
            minutes=minutes+1
        # reinitialise minutes, and count through hours until 12
        minutes=0
        hours=hours+1
    # show final position
    showhands(hours,minutes)