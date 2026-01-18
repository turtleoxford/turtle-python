import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    penup()
    MAXCOINS=20
    MAXTAKE=3
    COLUMNS=10
    MARGIN=35
    MENUTYPE=4
    MENUSIZE=36
    prob=[]
    for i in range(MAXCOINS):
        rowi=[5]*MAXTAKE
        prob.append(rowi)
        for j in range(MAXTAKE):
            if j>i:
                prob[i][j]=0
    taken=[0]*MAXCOINS
    numcoins=MAXCOINS
    h=1000/(COLUMNS+1)
    v=50
    r=(h*3)/8
    font=28
    youwin=0
    myscore=0
    yourscore=0
    opponent=0
    total=0

    def menu():
        blank(white)
        setxy(MARGIN,50)
        colour(brown)
        display('   NIM LEARNING PROGRAM',MENUTYPE|16,42)
        colour(darkred)
        setxy(MARGIN,150)
        display('This program learns to play NIM, and can be',MENUTYPE,32)
        setxy(MARGIN,200)
        display('configured to play either against you (human',MENUTYPE,32)
        setxy(MARGIN,250)
        display('opponent), or against a simulated computer',MENUTYPE,32)
        setxy(MARGIN,300)
        display('opponent, which either plays randomly or',MENUTYPE,32)
        setxy(MARGIN,350)
        display('itself learns from experience.',MENUTYPE,32)
        colour(black)
        setxy(MARGIN,525)
        display('Choose from the following:',MENUTYPE|16,MENUSIZE)
        setxy(MARGIN,650)
        display('  1. Human opponent',MENUTYPE,MENUSIZE)
        setxy(MARGIN,750)
        display('  2. Random opponent',MENUTYPE,MENUSIZE)
        setxy(MARGIN,850)
        display('  3. Opponent that also learns',MENUTYPE,MENUSIZE)

    def show():
        noupdate()
        blank(white)
        for i in range(MAXCOINS):
            setxy(3*h/2+(i%COLUMNS)*h,v+(i//COLUMNS)*v*(MAXTAKE+3))
            colour(red)
            blot(r)
            if i>=numcoins:
                colour(white)
                blot(r-3)
            movexy(-3*font/4,0)
            for j in range(MAXTAKE):
                movexy(0,v)
                colour(black)
                box(h/2,v,cream,True)
                if taken[i]==(j+1):
                    box(h/2,v,lime,True)
                elif taken[i]==-(j+1):
                    box(h/2,v,cyan,True)
                else:
                    box(h/2,v,cream,True)
                display(' '+str(prob[i][j]),4,font)
            if i%COLUMNS==0:
                setxy(h/2-font/2,v+(i/COLUMNS)*v*(MAXTAKE+3))
                colour(blue)
                for j in range(MAXTAKE):
                    movexy(0,v)
                    display(str(j+1),4,font)
        update()

    def coins(n):
        if n==1:
            result='1 coin'
        else:
            result=str(n)+' coins'
        return result

    def usermove(max):
        colour(black)
        setxy(h,v+(((MAXCOINS-1)//COLUMNS)+1)*v*(MAXTAKE+3))
        box(1000,500,white,False)
        if numcoins==1:
            display('Since there is only one coin left, you must take it',4,font)
            pause(200)
            result=1
        else:
            display('There are '+coins(numcoins)+', of which you may take up to '+str(max)+'.',4,font)
            movexy(0,v)
            display('How many would you like to take? ',4,font)
            keybuffer(10)
            n = 0
            while (n<=0) or (n>max):
                n = 0  # Reset n at the start of each iteration
                keys = read(10)
                for key in keys:
                    if key.isdigit():
                        digit = int(key)
                        if digit > 0 and digit <= max:
                            n = digit
                            break
                pause(10)  # Always pause to avoid freezing
            reset("keybuffer")
            movexy(0,v*2)
            display('OK - you are taking '+coins(n)+' ...',4,font)
            movexy(0,v)
            result=n
        return result

    def randommove(max):
        return randrange(max)+1

    def machinemove():
        total=0
        for i in range(MAXTAKE):
            total+=prob[numcoins-1][i]
        choose=randrange(total)
        i=0
        while ((choose>=0) and (i<max)):
            choose-=prob[numcoins-1][i]
            i+=1
        return i

    def showresult():
        if opponent==1:
            colour(black)
            setxy(200,v+(((MAXCOINS-1)//COLUMNS)+1)*v*(MAXTAKE+3))
            if youwin>0:
                display('YOU WIN!!',4,font*3)
            else:
                display(' I WIN!!',4,font*3)
            movexy(0,4*v)
            display('Press <RETURN> or <ENTER> to continue ...',4,font)
            keybuffer(10)
            reset("keybuffer")
            enter_pressed = False
            while not enter_pressed:
                keys = read(10)
                for key in keys:
                    if key == "Return":
                        enter_pressed = True
                        break
                pause(10)
            reset("keybuffer")
        else:
            print('PROGRAM: '+str(myscore)+';  OPPONENT: '+str(yourscore))

    def adjustweights():
        for i in range(MAXCOINS):
            if taken[i]!=0:
                if taken[i]*youwin>0:
                    add=1
                else:
                    add=-1
                for j in range(MAXTAKE):
                    if j<=i:
                        if ((j+1)==abs(taken[i])):
                            prob[i][j]+=add
                        else:
                            prob[i][j]-=add
                        if prob[i][j]<0:
                            prob[i][j]=0
                        if prob[i][j]>9:
                            prob[i][j]=9

    keyecho(False)
    menu()
    detect("key", 0)
    choice=abs(get_key_code())-48
    while (choice<=0) or (choice>=4):
        detect("key", 0)
        choice=abs(get_key_code())-48
    opponent=choice
    blank(white)
    while True:
        for i in range(MAXCOINS):
            taken[i]=0
        numcoins=MAXCOINS
        while numcoins>0: #!= 0
            show()
            if numcoins>MAXTAKE:
                max=MAXTAKE
            else:
                max=numcoins
            if opponent==1:
                move=usermove(max)
            elif opponent==2:
                move=randommove(max)
            else:
                move=machinemove()
            taken[numcoins-1]=move
            numcoins-=move
            if numcoins==0:
                youwin=1
            else:
                youwin=-1
                move=machinemove()
                if opponent==1:
                    pause(500)
                    show()
                    setxy(h,v+(((MAXCOINS-1)//COLUMNS)+1)*v*(MAXTAKE+3))
                    display('The computer will choose on these probabilities:',4,font)
                    movexy(0,v/2)
                    total=prob[numcoins-1][0]+prob[numcoins-1][1]+prob[numcoins-1][2]
                    for count in range(3):
                        movexy(0,v)
                        display('     '+coins(count+1)+': '+str(prob[numcoins-1][count])+'/'+str(total),4,font)
                    pause(500)
                    movexy(0,3*v/2)
                    display('OK, in response, the computer takes '+coins(move)+' ...',4,font)
                    pause(500)
                    reset("keybuffer")
                taken[numcoins-1]=-move
                numcoins-=move
            show()
        if youwin>0:
            yourscore+=1
        else:
            myscore+=1
        showresult()
        adjustweights()