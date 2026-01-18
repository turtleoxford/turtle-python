import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    MAXNODES=500
    SUFFNODES=400
    MAXEDGES=1000
    MINDISTANCE=40
    NODERADIUS=6
    ROADRADIUS=4
    NORMALROAD=black
    LINKROAD=blue
    nodex=[1]*MAXNODES
    nodey=[1]*MAXNODES
    nodedist=[1]*MAXNODES
    edge1=[1]*MAXNODES
    edge2=[1]*MAXNODES
    edgelen=[1]*MAXNODES

    def closest(n):
        result=0
        min=maxint()
        for i in range(numnodes):
            if i!=n:
                d=hypot(nodex[n]-nodex[i],nodey[n]-nodey[i])
                if d<min:
                    min=d
                    result=i
        if min<MINDISTANCE:
            result=-1
        return result

    def marknode(n,col,rad):
        setxy(nodex[n],nodey[n])
        colour(col)
        blot(rad)

    def makeedge(nodea,nodeb,col):
        global numedges
        numedges+=1
        edge1[numedges]=nodea
        edge2[numedges]=nodeb
        edgelen[numedges]=hypot(nodex[nodea]-nodex[nodeb],nodey[nodea]-nodey[nodeb])
        setxy(nodex[nodea],nodey[nodea])
        colour(col)
        setxy(nodex[nodeb],nodey[nodeb])
        polyline(2)

    def linkup(nodea,nodeb):
        global numnodes
        if hypot(nodex[nodea]-nodex[nodeb],nodey[nodea]-nodey[nodeb])<MINDISTANCE*2:
            makeedge(nodea,nodeb,NORMALROAD)
        else:
            numnodes+=1
            nodex[numnodes]=(nodex[nodea]+nodex[nodeb])/2
            nodey[numnodes]=(nodey[nodea]+nodey[nodeb])/2
            marknode(numnodes,cyan,ROADRADIUS)
            linkup(nodea,numnodes)
            linkup(numnodes,nodeb)

    def joinup(thisnode):
        for i in range(numnodes):
            nodedist[i]=maxint()
        nodedist[thisnode]=0
        cont=True
        while cont:
            cont=False
            for i in range(numedges):
                if nodedist[edge1[i]]<maxint():
                    if nodedist[edge1[i]]+edgelen[i]<nodedist[edge2[i]]:
                        nodedist[edge2[i]]=nodedist[edge1[i]]+edgelen[i]
                        cont=True
                if nodedist[edge2[i]]<maxint():
                    if nodedist[edge2[i]]+edgelen[i]<nodedist[edge1[i]]:
                        nodedist[edge1[i]]=nodedist[edge2[i]]+edgelen[i]
                        cont=True
        i=0
        cont=True
        while (i<numnodes) and cont:
            i+=1
            dist=hypot(nodex[i]-nodex[thisnode],nodey[i]-nodey[thisnode])
            if (i!=thisnode) and (nodedist[i]>1000) and (dist<MINDISTANCE*2):
                makeedge(thisnode,i,LINKROAD)
                cont=False

    thickness(6)
    numnodes=0
    numedges=0
    while numnodes<SUFFNODES:
        numnodes+=1
        m=closest(numnodes)
        while m<0:
            nodex[numnodes]=randrange(1000)
            nodey[numnodes]=randrange(1000)
            m=closest(numnodes)
        marknode(numnodes,red,NODERADIUS)
        if m>0:
            linkup(m,numnodes)
    for m in range(numnodes):
        joinup(m)