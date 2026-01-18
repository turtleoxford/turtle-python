import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    POLRADIUS=80
    MOLRADIUS=10
    HITRADIUS=90
    MOLECULES=400
    SLOWSPEED=30
    HIGHSPEED=50
    SPEEDRATIO=10
    POLCOLOUR=blue
    MOLCOLOUR=red
    HALOCOLOUR=16777214
    DELAY=50
    mx=[1]*MOLECULES
    my=[1]*MOLECULES
    ms=[1]*MOLECULES
    md=[1]*MOLECULES

    def draw(positive):
        if positive:
            colour(MOLCOLOUR)
        else:
            colour(white)
        for n in range(MOLECULES):
            setxy(mx[n],my[n])
            blot(MOLRADIUS)
        if positive:
            colour(POLCOLOUR)
        setxy(px,py)
        blot(POLRADIUS)

    noupdate()
    penup()
    px=500
    py=500
    pxvel=0
    pyvel=0
    setxy(px,py)
    colour(HALOCOLOUR)
    blot(HITRADIUS)
    for n in range(MOLECULES):
        while (pixcol(mx[n],my[n])!=white):
            mx[n]=randrange(1000-2*MOLRADIUS)+MOLRADIUS
            my[n]=randrange(1000-2*MOLRADIUS)+MOLRADIUS
        ms[n]=randrange(HIGHSPEED-SLOWSPEED+1)+SLOWSPEED
        md[n]=randrange(360)
        setxy(mx[n],my[n])
        blot(2*MOLRADIUS)
    blank(white)
    draw(True)
    while (abs(px-500)<=490) or (abs(py-500)<=480):
        noupdate()
        draw(False)
        for n in range(MOLECULES):
            setxy(mx[n],my[n])
            direction(md[n])
            forward(ms[n])
            if hypot(turtx()-px,turty()-py)<=HITRADIUS:
                while hypot(turtx()-px,turty()-py)<HITRADIUS:
                    back(1)
                turnxy(px-turtx(),py-turty())
                degturn=t._direction-md[n]
                md[n]=(180+(t._direction+degturn))%360
                impact=cos(degturn) * ms[n]
                pxvel=pxvel+sin(t._direction) * impact
                pyvel=pyvel-cos(t._direction) * impact
            mx[n]=(turtx()+1000)%1000
            my[n]=(turty()+1000)%1000
        px=px+pxvel/SPEEDRATIO
        py=py+pyvel/SPEEDRATIO
        draw(True)
        update()
        pause(DELAY)