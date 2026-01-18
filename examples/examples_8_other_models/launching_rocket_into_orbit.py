import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    earthradius=6371000
    earthgm=398600442
    initdirection=2000
    initthrust=20000
    thrusttime=500
    angleprecision=1296000

    def drawrocket():
        noupdate()
        blank(black)
        colour(teal)
        setxy(0,0)
        blot(earthradius/1000)
        setxy(x/1000,y/1000)
        direction(d)
        thickness(4)
        colour(silver)
        forward(200)
        back(200)
        if thrust>0:
            thickness(8)
            colour(yellow)
            back(200)
            forward(200)
        update()

    def report():
        print('')
        print('TIME = '+str(t))
        print(' Xposition = '+str(x)+' metres')
        print(' Yposition = '+str(y)+' metres')
        print(' Height = '+qstr(dist-earthradius,1000,2)+' km')
        print(' Direction = '+qstr(d,3600,1)+' degrees')
        print(' Thrust = '+qstr(thrust,1000,1)+' newtons per kg')
        print('  Xthrust = '+qstr(xthrust,1000,1)+' newtons per kg')
        print('  Ythrust = '+qstr(ythrust,1000,1)+' newtons per kg')
        print(' Gravity = '+qstr(gravity,1000,1)+' newtons per kg')
        print('  Xgravity = '+qstr(xgravity,1000,1)+' newtons per kg')
        print('  Ygravity = '+qstr(ygravity,1000,1)+' newtons per kg')
        print(' Xvelocity = '+qstr(xvel,1000,1)+' metres per s')
        print(' Yvelocity = '+qstr(yvel,1000,1)+' metres per s')

    canvas(-20000,-20000,40000,40000)
    angles(angleprecision)
    x=0
    y=-earthradius
    xvel=0
    yvel=0
    d=initdirection
    t=0
    prevdiff=1
    thrust=initthrust
    dist=earthradius
    while (dist>=earthradius) and (dist<40000000):
        drawrocket()
        prevdist=dist
        dist=hypot(x,y)
        if ((dist-prevdist)*prevdiff<=0) and (t>0):
            report()
        prevdiff=dist-prevdist
        gravity=divmult(earthgm,divmult(dist,1000000,dist),1000)
        xgravity=divmult(gravity,dist,-x)
        ygravity=divmult(gravity,dist,-y)
        xthrust=sin(d) * thrust
        ythrust=-cos(d) * thrust
        xvel=xvel+xgravity+xthrust
        yvel=yvel+ygravity+ythrust
        x=x+xvel/1000
        y=y+yvel/1000
        if yvel>0:
            d=angleprecision/2-atan(xvel/yvel)
        else:
            d=atan(xvel/-yvel)
        t+=1
        if t==thrusttime:
            thrust=0
    if dist<earthradius:
        colour(yellow)
        for explosion in range(100,200):
            blot(explosion)
            pause(3)
        colour(black)
        blot(200)