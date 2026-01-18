import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # draws n steps
    def steps(n):
        size=1000/n
        setxy(0,1000)
        thickness(1)
        for count in range(n*2):
            if count%2==1:
                movexy(0,-size)
            else:
                movexy(size,0)
        movexy(0,n*size)
        movexy(-n*size,0)
        colour(blue)
        polygon(n*2+2)

    # simulates the movement of a ball with the effect of gravity
    def throwBall(xVelocity, yVelocity, gravity, floor):
        # Move the ball until it reaches the specified floor level,
        setxy(t._x, t._y - 1)
        while t._y != floor:
            colour(white)
            blot(26)
            movexy(xVelocity, yVelocity)
            yVelocity = yVelocity + gravity
            # Clamp to floor if we've gone past it.
            if t._y > floor:
                setxy(t._x, floor)
            colour(red)
            blot(24)
            update()
            pause(10)
            noupdate()

    # draw steps
    steps(10)
    # set starting point
    setxy(950,75)
    # throw ball down each step
    while not(t._x<75):
        throwBall(-2,-22,1,t._y+100)
    # bounce ball on the ground
    for count in range(10):
        throwBall(0,count*2-18,1,t._y)