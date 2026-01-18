import sys
import os
import math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    xOrigin = 500
    yOrigin = 500
    halfWidth = 400
    yScale = 200
    radians =False # make true for x-axis in radians
    # draws graph axes
    def drawAxes():
        colour(black)
        thickness(3)
        # draw y axis
        setxy(xOrigin-halfWidth,yOrigin)
        drawxy(halfWidth*2,0)
        # draw x axis
        setxy(xOrigin,0)
        drawxy(0,1000)
        # draw circle at origin
        setxy(xOrigin,yOrigin)
        circle(15)
        # draw lines at y=1 and y=-1
        thickness(2)
        setxy(xOrigin-halfWidth,yOrigin-yScale)
        drawxy(halfWidth*2,0)
        setxy(xOrigin-halfWidth,yOrigin+yScale)
        drawxy(halfWidth*2,0)
        setxy(xOrigin+halfWidth+10,yOrigin-yScale-18)
        display('+1',0,20)
        setxy(xOrigin+halfWidth+10,yOrigin+yScale-18)
        display('-1',0,20)
        # print x axis labels
        if radians:
            setxy(xOrigin-halfWidth-44,yOrigin-4)
            display('-p',29,28)
            setxy(xOrigin-halfWidth//2-2,yOrigin-4)
            display('-p/2',29,28)
            setxy(xOrigin+halfWidth//2-50,yOrigin-4)
            display('p/2',29,28)
            setxy(xOrigin+halfWidth,yOrigin-4)
            display('p',29,28)
        else:
            setxy(xOrigin-halfWidth-60,yOrigin)
            display('-180',0,20)
            setxy(xOrigin-halfWidth//2,yOrigin)
            display('-90',0,20)
            setxy(xOrigin+halfWidth//2-30,yOrigin)
            display('90',0,20)
            setxy(xOrigin+halfWidth,yOrigin)
            display('180',0,20)

    # plots a sine curve
    def plotSineCurve():
        for degrees in range(-180,181,1):
            x=xOrigin+divmult(degrees,180,halfWidth)
            y=yOrigin - (math.sin(math.radians(degrees)) * yScale)
            setxy(x,y)
        polyline(361)

    # plots a cosine curve
    def plotCosineCurve():
        for degrees in range(-180,181,1):
            x=xOrigin+divmult(degrees,180,halfWidth)
            y=yOrigin - (math.cos(math.radians(degrees)) * yScale)
            setxy(x,y)
        polyline(361)

    # plots a tan curve
    def plotTanCurve():
        for degrees in range(-180,181,1):
            if degrees==-90:
                polyline(90)
            else:
                if degrees==90:
                    polyline(179)
                else:
                    x=xOrigin+divmult(degrees,180,halfWidth)
                    y=yOrigin - (math.tan(math.radians(degrees)) * yScale)
                    setxy(x,y)
        polyline(90)

    # draw axes
    drawAxes()
    noupdate()
    thickness(4)
    # plot sine curve in green
    colour(green)
    setxy(250,700)
    display('sine',16,40)
    plotSineCurve()
    # plot cosine curve in red
    colour(red)
    setxy(30,700)
    display('cosine',16,40)
    plotCosineCurve()
    # plot tan curve in blue
    colour(blue)
    setxy(140,920)
    display('tangent',16,40)
    plotTanCurve()