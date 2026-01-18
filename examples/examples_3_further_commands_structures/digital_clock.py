import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # prints the specified time inside a white box in the canvas
    def showtime(hours,minutes):
        # draw white box, erasing previous time
        setxy(300,430)
        box(400,130,white,False)
        # print specified time
        timeString=pad(str(hours),'0',2)+':'+pad(str(minutes),'0',2)
        display(timeString,21,100)

    # set up canvas with box for displaying time
    blank(lightgreen)
    setxy(250,400)
    # Turtle maroon pen thickness 10 will be used for box border
    colour(maroon)
    thickness(10)
    # box will be size 500x200, filled in lightbrown with a border
    box(500,200,lightbrown,True)
    colour(black)
    # initialise hours and minutes to zero
    hours=0
    minutes=0
    # repeatedly through the hours
    while hours<12:
        # display the current time
        showtime(hours,minutes)
        # pause 1/10 second [so clock goes 600 times too fast]
        pause(100)
        # increment the minutes, ...
        minutes=minutes+1
        if minutes==60:
            # if necessary, move on to the next hour
            hours=hours+1
            minutes=0
    # show final time
    showtime(hours,minutes)