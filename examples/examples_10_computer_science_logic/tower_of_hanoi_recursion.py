import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    delay=500
    pile=['','','']
    x=[250,500,750]
    y=[800,500,800]
    top=[0,0,0]

    def getnum(prompt):
        print(prompt, end="")
        s='3'
        while '012'.find(s)<0:
            s=input()
        return ord(s[0])-48

    def setup(startdisk):
        for p in range(3):
            top[p]=y[p]-numdisks*20-40
        for d in range(numdisks):
            pile[startdisk]=pile[startdisk]+chr(d+49)
        print(pad(' ',' ',-32)+'   PILE 0   PILE 1   PILE 2')
        print()
        print(pad('Starting position:',' ',-32), end='')
        print(pad(pile[0],' ',9)+pad(pile[1],' ',9)+pad(pile[2],' ',9))
        print()

    def draw():
        for p in range(3):
            setxy(x[p],y[p])
            for i in range(len(pile[p])-1,-1,-1):
                movexy(0,-20)
                colour(rgb(ord(pile[p][i])-47))
                ellblot((ord(pile[p][i])-46)*20,(ord(pile[p][i])-46)*10)
            colour(black)
            setxy(x[p],top[p])
            polyline(2)

    def movedisk(n,start,finish):
        global count
        pile[finish]=pile[start][0]+pile[finish]
        pile[start]=pile[start][1:len(pile[start])]
        blank(white)
        draw()
        count+=1
        print(pad(str(count),' ',4)+'. Move disk '+str(n)+' from '+str(start)+' to '+str(finish)+':  ', end='')
        print(pad(pile[0],' ',9)+pad(pile[1],' ',9)+pad(pile[2],' ',9))
        pause(delay)

    def movepile(n,start,finish):
        if n>0:
            movepile(n-1,start,3-start-finish)
            movedisk(n,start,finish)
            movepile(n-1,3-start-finish,finish)

    numdisks=0
    while numdisks<2:
        print('TOWER OF HANOI')
        print()
        numdisks= intdef(input('How many disks would you like in the tower? (minimum 2, maximum 48) '),0)
        numdisks=min(max(numdisks,2),48) # Clamp to range 2 to 48
    start=getnum('Start pillar (0, 1, or 2)? ')
    finish=getnum('Finish pillar (0, 1 or 2)? ')
    setup(start)
    thickness(10)
    draw()
    pause(1000)
    count=0
    movepile(numdisks,start,finish)