import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(800, 600) as t:
    colour('black')
    
    cols=10
    rows=10
    a=3
    b=4
    fname='SaveCSV.csv'
    value=[]
    for i in range(rows):
        toadd=[0]*cols
        value.append(toadd)
    colwidth=800/(cols+1)
    rowheight=500/(rows+1)
    xmargin=colwidth*3/7
    ymargin=rowheight/3
    fontsize=colwidth/4

    def drawgrid(): #draw the grid lines
        for i in range(cols+2):
            if (i==0) or (i==1) or (i==cols+1):
                thickness(10)
            else:
                thickness(2)
            setxy(5+i*colwidth,5)
            drawxy(0,890)
        for j in range(rows+1):
            if (j==0) or (j==1) or (j==rows+1):
                thickness(10)
            else:
                thickness(2)
            setxy(5,5+j*rowheight)
            drawxy(995,0)

    def labelgrid(): #add the grid headings
        setxy(colwidth-25,5)
        display('x',0,30)
        setxy(20,rowheight-45)
        display('y',0,30)
        setxy(300,925)
        display('Table of '+str(a)+'x + '+str(b)+'y',0,40)
        for i in range(cols):
            setxy((i+1)*colwidth+xmargin,ymargin)
            display(str(i+1),0,fontsize)
        for j in range(rows):
            setxy(xmargin,(j+1)*rowheight+ymargin)
            display(str(j+1),0,fontsize)

    def calculate(): #calculate the array values
        for i in range(cols):
            for j in range(rows):
                value[i][j]=a*(i+1)+b*(j+1)

    def show(): #put array values in grid
        for i in range(cols):
            for j in range(rows):
                setxy((i+1)*colwidth+xmargin,(j+1)*rowheight+ymargin)
                display(str(value[i][j]),0,fontsize)

    def savedata(): #save values as CSV file
        if isfile(fname):
            flag=fremove(fname)
        handle=fopen(fname,3)
        for j in range(rows):
            for i in range(cols-1):
                fwrite(handle,str(value[i][j])+',')
            fwriteline(handle,str(value[cols-1][j]))
        fclose(handle)

    drawgrid()
    labelgrid()
    calculate()
    show()
    pause(2000)
    savedata()
    print('File '+fname+' has been saved')