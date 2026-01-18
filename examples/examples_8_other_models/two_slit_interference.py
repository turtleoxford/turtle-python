import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    SECTORS=7
    WAVELENGTH=100
    SOURCEY=730
    SOURCE1X=275
    SOURCE2X=725
    lampx=1
    x=1
    y=1
    disty=1
    dist1=1
    dist2=1
    wave1=1
    wave2=1
    waveaddi=1
    waveaddj=1
    waveadd=1
    angleadd=1
    sectcol=[0]*(SECTORS+1)
    boundary=[0]*(SECTORS+1)

    def colsetup():
        sectcol[0]=violet
        sectcol[1]=blue
        sectcol[2]=cyan
        sectcol[3]=lime
        sectcol[4]=yellow
        sectcol[5]=orange
        sectcol[6]=red
        sectcol[7]=violet
        for n in range(SECTORS+1):
            boundary[n]=int(divmult(360,SECTORS,n))

    def wavecolour(n):
        col2=1
        while boundary[col2]<n:
            col2+=1
        col1=col2-1
        return mixcols(sectcol[col1],sectcol[col2],boundary[col2]-n,n-boundary[col1])

    def background():
        lampx=(SOURCE1X+SOURCE2X)/2
        blank(black)
        colour(white)
        thickness(5)
        setxy(0,733)
        drawxy(1000,0)
        setxy(SOURCE1X,732)
        for dist1 in range(1,5,1):
            colour(wavecolour(WAVELENGTH-dist1))
            drawxy(0,1)
        diagx=lampx-SOURCE1X
        diag=hypot(diagx,250)
        for n in range(1,251,1):
            dist1=divmult(diag,250,n)
            wave1=WAVELENGTH-((dist1+5)%WAVELENGTH)
            colour(wavecolour(divmult(wave1,WAVELENGTH,360)))
            drawxy(SOURCE1X+divmult(diagx,250,n)-turtx(),1)
        setxy(SOURCE2X,732)
        for dist2 in range(1,5,1):
            colour(wavecolour(WAVELENGTH-dist2))
            drawxy(0,1)
        diagx=SOURCE2X-lampx
        diag=hypot(diagx,250)
        for n in range(1,251,1):
            dist2=divmult(diag,250,n)
            wave2=WAVELENGTH-((dist2+5)%WAVELENGTH)
            colour(wavecolour(divmult(wave2,WAVELENGTH,360)))
            drawxy(SOURCE2X-divmult(diagx,250,n)-turtx(),1)
        colour(yellow)
        setxy(lampx,984)
        blot(10)

    colsetup()
    background()
    noupdate()
    for y in range(0,SOURCEY+1,1):
        disty=SOURCEY-y
        for x in range(1000):
            dist1=hypot(x-SOURCE1X,disty)
            dist2=hypot(x-SOURCE2X,disty)
            wave1=dist1%WAVELENGTH
            wave2=dist2%WAVELENGTH
            waveaddi=sin(wave1*360/WAVELENGTH) * 500 + sin(wave2*360/WAVELENGTH) * 500
            waveaddj=cos(wave1*360/WAVELENGTH) * 500 + cos(wave2*360/WAVELENGTH) * 500
            waveadd=hypot(waveaddi,waveaddj)
            angleadd=(atan(waveaddi/waveaddj)+360)%360
            pixset(x,y,mixcols(wavecolour(angleadd),black,waveadd,1000-waveadd))