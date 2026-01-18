import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    MAXANIMALS=500
    MINGAZELLES=10
    STARTCHEETAHS=50
    STARTGAZELLES=50
    MAXSPEED=1000
    STARTSLOW=30
    STARTFAST=70
    RANDMARGINC=10
    RANDMARGING=10
    HUNTINGTRIES=100
    CATCHMARGIN=5
    CFOODADD=40
    CBREEDFOOD=10
    CMATINGRATIO=2
    GMATINGRATIO=1
    CHUNTINGRATIO=1
    SLOWAGE=100
    AGEFACTOR=0
    GRAPHLEFT=60
    GRAPHWIDTH=900
    GRAPHHEIGHT=400
    CGRAPHBASE=450
    GGRAPHBASE=950
    YMAX=20
    gen=0
    cnum=STARTCHEETAHS
    gnum=STARTGAZELLES
    cspeed=[0]*MAXANIMALS
    gspeed=[0]*MAXANIMALS
    cgenspeed=[0]*MAXANIMALS
    ggenspeed=[0]*MAXANIMALS
    cage=[0]*MAXANIMALS
    gage=[0]*MAXANIMALS
    cfood=[1]*MAXANIMALS
    cspeednum=[0]*(MAXSPEED+1)
    gspeednum=[0]*(MAXSPEED+1)

    def setup():
        for n in range(0,cnum,1):
            cgenspeed[n]=randrange(STARTFAST+1-STARTSLOW)+STARTSLOW
            cspeed[n]=cgenspeed[n]
            cage[n]=randrange(SLOWAGE)
            cfood[n]=randrange(CFOODADD)+1
            cspeednum[cspeed[n]]+=1
        for n in range(cnum+1,MAXANIMALS,1):
            cspeed[n]=0
        for n in range(1,gnum,1):
            ggenspeed[n]=randrange(STARTFAST+1-STARTSLOW)+STARTSLOW
            gspeed[n]=ggenspeed[n]
            gage[n]=randrange(SLOWAGE)
            gspeednum[gspeed[n]]+=1
        for n in range(gnum+1,MAXANIMALS,1):
            gspeed[n]=0

    def axes(graphbase):
        colour(black)
        setxy(GRAPHLEFT,graphbase-GRAPHHEIGHT)
        drawxy(0,GRAPHHEIGHT)
        drawxy(GRAPHWIDTH,0)
        for n in range(0,11,1):
            setxy(20,graphbase-n*GRAPHHEIGHT/10-19)
            display(str(n*YMAX/10),0,20)
        for n in range(1,11,1):
            setxy(GRAPHLEFT+n*GRAPHWIDTH/10-20,graphbase)
            display(str(n*MAXSPEED/10),0,20)

    def graph():
        noupdate()
        blank(white)
        axes(450)
        axes(950)
        setxy(200,20)
        colour(red)
        display('Speed Distribution of Cheetahs',4,25)
        setxy(750,20)
        display(str(cnum),4,25)
        ctotal=0
        for n in range(1,MAXSPEED,1):
            setxy(GRAPHLEFT+n*GRAPHWIDTH/MAXSPEED,450)
            drawxy(0,-GRAPHHEIGHT*cspeednum[n]/YMAX)
            ctotal=ctotal+n*cspeednum[n]
        setxy(200,520)
        colour(green)
        display('Speed Distribution of Gazelles',4,25)
        setxy(750,520)
        display(str(gnum),4,25)
        gtotal=0
        for n in range(1,MAXSPEED,1):
            setxy(GRAPHLEFT+n*GRAPHWIDTH/MAXSPEED,950)
            drawxy(0,-GRAPHHEIGHT*gspeednum[n]/YMAX)
            gtotal=gtotal+n*gspeednum[n]
        setxy(850,20)
        if cnum<1:
            setxy(150,200)
            colour(magenta)
            display('All Cheetahs Have Died',4,50)
            halt()
        display(qstr(ctotal,cnum,2),4,25)
        setxy(850,520)
        display(qstr(gtotal,gnum,2),4,25)
        update()
        print(str(gen)+' - c='+str(cnum)+' (av='+qstr(ctotal,cnum,2)+')')
        update()
        noupdate()
        print('     g='+str(gnum)+'  (av='+qstr(gtotal,gnum,2)+')')

    def deadcheetah(c):
        global cnum
        cspeednum[cspeed[c]]-=1
        cspeed[c]=0
        cnum-=1

    def deadgazelle(g):
        global gnum
        gspeednum[gspeed[g]]-=1
        gspeed[g]=0
        gnum-=1

    def babycheetah(speed):
        global cnum
        b=1
        while (cspeed[b]!=0) and (b!=MAXANIMALS-1):
            b+=1
        if cspeed[b]==0:
            cnum+=1
            cgenspeed[b]=speed+randrange(2*RANDMARGINC+1)-RANDMARGINC
            cgenspeed[b]=max(1,min(MAXSPEED,cgenspeed[b]))
            cspeed[b]=cgenspeed[b]
            cage[b]=0
            cfood[b]=CFOODADD
            cspeednum[cspeed[b]]+=1

    def babygazelle(speed):
        global gnum
        b=1
        while (gspeed[b]!=0) and (b!=MAXANIMALS-1):
            b+=1
        if gspeed[b]==0:
            gnum+=1
            ggenspeed[b]=speed+randrange(2*RANDMARGING+1)-RANDMARGING
            ggenspeed[b]=max(1,min(MAXSPEED,ggenspeed[b]))
            gspeed[b]=ggenspeed[b]
            gage[b]=0
            gspeednum[gspeed[b]]+=1

    def generation():
        for c in range(1,round(cnum/CHUNTINGRATIO),1):
            c=randrange(MAXANIMALS)
            if (cspeed[c]>0) and (gnum>MINGAZELLES):
                tries=1
                g=randrange(MAXANIMALS)
                while (gspeed[g]<=0) and (tries!=HUNTINGTRIES):
                    tries+=1
                    g=randrange(MAXANIMALS)
                if (gspeed[g]>0) and (cspeed[c]>=gspeed[g]+CATCHMARGIN):
                    deadgazelle(g)
                    cfood[c]=cfood[c]+CFOODADD
        for n in range(1,round(cnum/CMATINGRATIO),1):
            c=randrange(MAXANIMALS)
            if (cnum<MAXANIMALS) and (cspeed[c]>0) and (cfood[c]>=CBREEDFOOD):
                babycheetah(cgenspeed[c])
                cfood[c]=cfood[c]-CBREEDFOOD
        for n in range(1,round(gnum/GMATINGRATIO),1):
            g=randrange(MAXANIMALS)
            if (gnum<MAXANIMALS) and (gspeed[g]>0):
                babygazelle(ggenspeed[g])
        for n in range(0,MAXANIMALS,1):
            if cspeed[n]>0:
                cage[n]+=1
                if cage[n]>SLOWAGE:
                    cspeednum[cspeed[n]]-=1
                    cspeed[n]=int(cspeed[n]*AGEFACTOR/100)
                    cspeednum[cspeed[n]]+=1
                    if cspeed[n]==0:
                        deadcheetah(n)
                cfood[n]-=1
                if cfood[n]<0:
                    deadcheetah(n)
            if gspeed[n]>0:
                gage[n]+=1
                if gage[n]>SLOWAGE:
                    gspeednum[gspeed[n]]-=1
                    gspeed[n]=int(gspeed[n]*AGEFACTOR/100)
                    gspeednum[gspeed[n]]+=1
                    if gspeed[n]==0:
                        deadgazelle(n)

    setup()
    graph()
    while True:
        gen+=1
        generation()
        graph()