import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    WIDTH=10
    HEIGHT=10
    MAXLAST=255
    DELAY=0
    MARGIN=20
    TIMELIMIT=600
    PAUSEONBEST=1000
    DRAWALL=False
    vectorx=[1,2,2,1,-1,-2,-2,-1]
    vectory=[-2,-1,1,2,2,1,-1,-2]
    squarestatus=[0]*MAXLAST
    cleverrank=[0]*MAXLAST
    lastsquare=WIDTH*HEIGHT-1
    xgap=(1000-2*MARGIN)/WIDTH
    ygap=(1000-2*MARGIN)/HEIGHT
    if xgap<=ygap:
        radius=xgap*2/5
    else:
        radius=ygap*2/5

    def findx(s):
        return s%WIDTH

    def findy(s):
        return s//WIDTH

    def findsquare(x,y):
        return y*WIDTH+x

    def drawsquare(s):
        setxy(MARGIN+xgap*findx(s)+xgap/2,MARGIN+ygap*findy(s)+ygap/2)
        if squarestatus[s]==0:
            colour(salmon)
            blot(radius)
        else:
            colour(white)
            blot(radius)
            if WIDTH>10:
                if squarestatus[s]<10:
                    movexy(-8,-20)
                elif squarestatus[s]<100:
                    movexy(-15,-20)
                else:
                    movexy(-22,-20)
                colour(black)
                display(str(squarestatus[s]),4,20)
            else:
                if squarestatus[s]<10:
                    movexy(-10,-24)
                elif squarestatus[s]<100:
                    movexy(-20,-24)
                else:
                    movexy(-30,-24)
                colour(black)
                display(str(squarestatus[s]),4,25)

    def drawboard():
        blank(darkgreen)
        for s in range(lastsquare+1):
            drawsquare(s)

    def goodmove(s,direction):
        newx=findx(s)+vectorx[direction]
        newy=findy(s)+vectory[direction]
        if (newx>=0) and (newx<WIDTH) and (newy>=0) and (newy<HEIGHT):
            result=findsquare(newx,newy)
            if squarestatus[result]>0:
                result=-1
        else:
            result=-1
        return result

    def moveto(s,direction):
        newx=findx(s)+vectorx[direction]
        newy=findy(s)+vectory[direction]
        result=findsquare(newx,newy)
        if clever:
            for d in range(8):
                newn=goodmove(result,d)
                if newn>-1: #check this
                    cleverrank[newn]-=1
        return result

    def clearboard():
        for s in range(lastsquare+1):
            squarestatus[s]=0
        if clever:
            for s in range(lastsquare+1):
                cleverrank[s]=0
                for d in range(8):
                    if goodmove(s,d)>-1: #check this
                        cleverrank[s]+=1

    def randommove(s):
        d=randrange(8)
        while (goodmove(s,d)<=-1) and (time()<TIMELIMIT): #check this
            d=randrange(8)
        return d

    def clevermove(s):
        chosen=-1
        bestrank=9
        for d in range(8):
            news=goodmove(s,d)
            if news>-1: #check this
                if cleverrank[news]<bestrank:
                    chosen=d
                    bestrank=cleverrank[news]
                    numbest=1
                elif cleverrank[news]==bestrank:
                    numbest+=1
                    if randrange(numbest)==0:
                        chosen=d
        return chosen

    def findroute():
        countsquares=1
        thiss=randrange(lastsquare+1)
        squarestatus[thiss]=countsquares
        timeset(0)
        while time()<TIMELIMIT:
            if clever:
                d=clevermove(thiss)
            else:
                d=randommove(thiss)
            if (time()<TIMELIMIT) and (d>-1):
                thiss=moveto(thiss,d)
                countsquares+=1
                squarestatus[thiss]=countsquares
                if DRAWALL:
                    drawsquare(thiss)
        return countsquares

    print('Random search or Clever search? (R/C) ')
    det=detect("key",0).lower()
    while (det!="r") and (det!="c"):
        det=detect("key",0).lower()
    clever=(det=="c")
    if clever:
        print('  Clever ...')
    else:
        print('  Random ...')
    if lastsquare>MAXLAST:
        print('Error: maximum board size is '+str(MAXLAST+1)+' squares')
    else:
        attempts=0
        total=0
        best=0
        first=True
        while first or (best!=WIDTH*HEIGHT):
            first=False
            attempts+=1
            clearboard()
            if DRAWALL:
                drawboard()
            countsquares=findroute()
            total=total+countsquares
            pausenow=(countsquares>best)
            if countsquares>best:
                drawboard()
                best=countsquares
                if attempts>1:
                    print('Attempt '+str(attempts)+', score: '+str(countsquares)+'  (average of all attempts: '+qstr(total,attempts,2)+')')
                else:
                    print('Attempt '+str(attempts)+', score: '+str(countsquares))
                update()
            if pausenow:
                pause(PAUSEONBEST)
            noupdate()