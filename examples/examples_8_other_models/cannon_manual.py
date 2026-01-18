import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:   
    canvas(0,0,10500,10000)
    # Constants
    gunlength=1000
    distancecol=green
    timecol=red

    # Draw axes of graph
    def graphaxes():
        thickness(5)
        setxy(9700,600)
        drawxy(0,3900)
        drawxy(-9000,0) # x axis 700 to 9700
        drawxy(0,-3900) # y axis 4500 to 600
        for n in range(0,91,5):
            setxy(650+n*100,4600)
            display(str(n),"Arial",16)
        for n in range(10):
            setxy(100,4350-n*400)
            display(str(n*1000),"Arial",16)
        for n in range(10):
            setxy(9900,4380-n*400)
            display(str(n*20),"Arial",16)
        setxy(4000,4900)
        display("Angle of elevation","Arial",24)
        colour(distancecol)
        setxy(0,100)
        display("Distance","Arial",24)
        colour(timecol)
        setxy(9600,100)
        display("Time","Arial",24)

    # Plot coloured point on graph
    def plot(x,y,col):
        setxy(700+x*100,4500-y*2/5)
        colour(col)
        blot(40)

    # Draw cannon and aim by clicking on cream-coloured arc
    def aim():
        clickcol=white
        while clickcol!=red:
            if clickcol==cream:
                if (get_clickx()>=250) and (get_clicky()<=9750):
                    turnxy(get_clickx()-250,get_clicky()-9750)
            noupdate()
            setxy(0,10000)
            colour(cream)
            blot(1600)
            colour(yellowgreen)
            blot(1400)
            colour(maroon)
            setxy(250,9750)
            blot(250)
            forward(gunlength)
            setxy(250,9750)
            colour(red)
            blot(100)
            update()
            detect("mouse1",0)
            clickcol=pixcol(get_clickx(),get_clicky())

    # Fire the cannon
    def fire(xvel,yvel,gravity,floor):
        global steps
        setxy(250,9750)
        steps=0
        while (turty()!=floor):
            steps=steps+1
            if (pixcol(turtx(),turty())==black):
                colour(white)
                blot(90)
            movexy(xvel,yvel)
            yvel=yvel+gravity
            if (turty()>floor):
                sety(floor)
            if ((pixcol(turtx(),turty())==white) or (turty()==floor)):
                colour(black)
                blot(75)
            update()
            pause(10)
            noupdate()

    # Set up Canvas, initialise angle to 45 degrees, and loop
    canvas(0,0,10500,10000)
    graphaxes()
    direction(45)
    thickness(20)
    while (1==1):
        aim()
        print("Elevation: "+str(90-t._direction), end="")
        fire(cos(90-t._direction)*96,sin(90-t._direction)*-96,1,9950)
        print("  Distance: "+str(turtx())," Time: "+str(steps))
        plot(90-t._direction,turtx(),distancecol)
        plot(90-t._direction,steps*50,timecol)