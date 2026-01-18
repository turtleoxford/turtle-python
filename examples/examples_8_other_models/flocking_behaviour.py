import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    NUMBOIDS=30
    BOIDRADIUS=20
    MAXSPEED=50
    BOIDCOLOUR=lightbrown
    HALOCOLOUR=16777214
    DELAY=50
    POSFACTOR=50
    VELFACTOR=50
    NEARD=200
    NEARFACTOR=10
    TGTRADIUS=2000
    boidx=[1]*NUMBOIDS
    boidy=[1]*NUMBOIDS
    boidvx=[1]*NUMBOIDS
    boidvy=[1]*NUMBOIDS
    avgx=1
    avgy=1
    avgvx=1
    avgvy=1
    tgtx=1
    tgty=1
    tgtangvel=1
    cycle=0

    def setup():
        penup()
        colour(HALOCOLOUR)
        for n in range(NUMBOIDS):
            while (pixcol(boidx[n],boidy[n])!=white):
                boidx[n]=randrange(5000-2*BOIDRADIUS)+BOIDRADIUS
                boidy[n]=randrange(5000-2*BOIDRADIUS)+BOIDRADIUS
            boidvx[n]=randrange(MAXSPEED*2+1)-MAXSPEED
            boidvy[n]=randrange(MAXSPEED*2+1)-MAXSPEED
            blot(2*BOIDRADIUS)

    def draw(positive):
        if positive:
            colour(BOIDCOLOUR)
        else:
            colour(white)
        for n in range(NUMBOIDS):
            setxy(boidx[n],boidy[n])
            blot(BOIDRADIUS)

    def averages():
        global avgx, avgy, avgvx, avgvy
        totalx=0
        totaly=0
        totalvx=0
        totalvy=0
        for n in range(NUMBOIDS):
            totalx+=boidx[n]
            totaly+=boidy[n]
            totalvx+=boidvx[n]
            totalvy+=boidvy[n]
        avgx=totalx/NUMBOIDS
        avgy=totaly/NUMBOIDS
        avgvx=totalvx/NUMBOIDS
        avgvy=totalvy/NUMBOIDS

    def settarget():
        global cycle, tgtangvel, tgtx, tgty
        if cycle%100==0:
            tgtangvel=randrange(7)-3
        tgtx=divmult(sin(cycle*tgtangvel) * 1000,1000,TGTRADIUS)
        tgty=-divmult(cos(cycle*tgtangvel) * 1000,1000,TGTRADIUS)
        cycle+=1

    def move(b):
        boidvx[b]+=(avgx-boidx[b])/POSFACTOR+(avgvx-boidvx[b])/VELFACTOR
        boidvy[b]+=(avgy-boidy[b])/POSFACTOR+(avgvy-boidvy[b])/VELFACTOR
        for n in range(NUMBOIDS):
            if n!=b:
                distx=boidx[n]-boidx[b]
                disty=boidy[n]-boidy[b]
                if hypot(distx,disty)<NEARD:
                    boidvx[b]-=sign(distx)*(NEARD-abs(distx))/NEARFACTOR
                    boidvy[b]-=sign(disty)*(NEARD-abs(disty))/NEARFACTOR
        if randrange(10)==0:
            boidvx[b]=tgtx-boidx[b]
            boidvy[b]=tgty-boidy[b]
        speed=hypot(boidvx[b],boidvy[b])
        if speed>MAXSPEED:
            boidvx[b]=divmult(boidvx[b],speed,MAXSPEED)
            boidvy[b]=divmult(boidvy[b],speed,MAXSPEED)
        boidx[b]+=boidvx[b]
        boidy[b]+=boidvy[b]

    canvas(-2500,-2500,5000,5000)
    noupdate()
    setup()
    blank(white)
    draw(True)
    while (True):
        averages()
        settarget()
        noupdate()
        draw(False)
        for n in range(NUMBOIDS):
            move(n)
        draw(True)
        update()
        pause(DELAY)