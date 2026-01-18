import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    POPULATION=1000
    MATEPERGEN=400
    RANDOMVAR=1
    LEFTMARGIN=70
    TOPMARGIN=20
    female=[1]*POPULATION
    fop=[1]*POPULATION

    def axes():
        for i in range(1,10,1):
            setxy(LEFTMARGIN+i*100-25,TOPMARGIN+800)
            display(str(i*100),4,20)
        for i in range(2,11,1):
            setxy(0,1000-i*100)
            colour(black)
            display(str(i*10)+'%',4,20)
            movexy(LEFTMARGIN,TOPMARGIN)
            colour(lightgrey)
            drawxy(1000-LEFTMARGIN,0)
        setxy(LEFTMARGIN,TOPMARGIN)
        colour(black)
        drawxy(0,800)
        drawxy(1000-LEFTMARGIN,0)
        colour(red)
        setxy(50,880)
        display('Proportion of Females in Population, over 900 Generations',4,25)
        setxy(50,930)
        display('with Female Offspring Probability genes initially set 90%+',4,25)

    def graph():
        females=0
        for n in range(0,POPULATION,1):
            if female[n]==1:
                females+=1
        colour(red)
        setxy(LEFTMARGIN+generation,TOPMARGIN+1000-females)
        if generation>0:
            polyline(2)

    def domating():
        a=randrange(POPULATION)
        b=randrange(POPULATION)
        while female[a]==female[b]:
            a=randrange(POPULATION)
            b=randrange(POPULATION)
        inherita=(randrange(2)==0)
        replace=randrange(POPULATION)
        if inherita:
            fop[replace]=fop[a]
        else:
            fop[replace]=fop[b]
        female[replace]=fop[replace]>randrange(1000)
        fop[replace]=fop[replace]+randrange(RANDOMVAR*20+1)-RANDOMVAR*10
        fop[replace]=max(0,min(1000,fop[replace]))

    axes()
    for n in range(POPULATION):
        female[n]=(randrange(2)==0)
        fop[n]=900+randrange(101)
    generation=0
    while generation!=900:
        graph()
        generation+=1
        for n in range(MATEPERGEN):
            domating()