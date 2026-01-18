import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(800, 600) as t:
    colour('black')
    cols=10
    rows=10
    fname='SaveCSV.csv'
    value=[]
    for i in range(rows):
        toadd=[0]*cols
        value.append(toadd)
    colwidth=800/(cols+1)
    rowheight=600/(rows+1)
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
        display('Table read from file',0,40)
        for i in range(cols):
            setxy((i+1)*colwidth+xmargin,ymargin)
            display(str(i+1),0,fontsize)
        for j in range(rows):
            setxy(xmargin,(j+1)*rowheight+ymargin)
            display(str(j+1),0,fontsize)

    def show(): #put array values in grid
        for i in range(cols):
            for j in range(rows):
                setxy((i+1)*colwidth+xmargin,(j+1)*rowheight+ymargin)
                display(str(value[i][j]),0,fontsize)

    def readdata(): #read data from file

        def nextbit(s):
            posn=s.find(',')
            if posn==-1:
                result=s
                s=''
            else:
                result=s[:posn]
                s=s[posn+1:]
            return result

        i=0
        handle=fopen(fname,1)
        while not eof(handle):
            thisline=freadline(handle)
            j=0
            while thisline!='':
                thisbit=nextbit(thisline)
                thisline=thisline[len(thisbit)+1:]
                value[i][j]=intdef(thisbit,0)
                j+=1
            i+=1
        fclose(handle)

    drawgrid()
    labelgrid()
    readdata()
    show()
    pause(2000)
    print('File '+fname+' has been read')