import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    penup()
    MARGIN=35
    TAPELABEL=25
    TAPETOP=100
    CYCLEINDENT=200
    CYCLELABEL=200
    TABLELABEL=350
    TABLETOP=425
    ROWHEIGHT=48
    HEADSPACE=6
    FONTSIZE=23
    MENUSIZE=36
    FONTTYPE=16
    MENUTYPE=4
    LEFTEND=0
    RIGHTEND=500
    SHOWCELLS=20
    SHOWLEFTMIN=1
    SHOWLEFT=4
    SHOWRIGHT=2
    MAXSTATES=30
    MAXBEHAVIOUR=100
    MAXTRIGGERS=5
    tape=[' ']*RIGHTEND
    numstates=0
    state=-1
    machinetitle=''
    pausetime=200
    statecodes=''
    behaviour=['']*MAXSTATES
    triggerstring=['']*MAXSTATES
    transitionstring=['']*MAXSTATES
    cycles=0
    cellwidth=998/SHOWCELLS
    cmargin=cellwidth/4
    lmargin=(1000-SHOWCELLS*cellwidth)/2

    def definemachine(choice):
        global numstates
        global machinetitle
        if choice==1:
            machinetitle='Petzold p. 81, 0 1 0 1 ... 4 states'
            numstates=4
            behaviour[0]='b; cP0,R'
            behaviour[1]='c; eR'
            behaviour[2]='e; fP1,R'
            behaviour[3]='f; bR'
        elif choice==2:
            machinetitle='Petzold p. 84, 0 1 0 1 ... 1 state'
            numstates=1
            behaviour[0]='b; bP0;0bR,R,P1;1bR,R,P0;'
        elif choice==3:
            machinetitle='Petzold p. 87, transcendental'
            numstates=5
            behaviour[0]='b;*oP@,R,P@,R,P0,R,R,P0,L,L'
            behaviour[1]='o;1oR,Px,L,L,L;0q'
            behaviour[2]='q; pP1,L;*qR,R'
            behaviour[3]='p;xqP ,R;@fR; pL,L'
            behaviour[4]='f; oP0,L,L;*fR,R'
        elif choice==4:
            machinetitle='Petzold p. 99, binary counting'
            numstates=3
            behaviour[0]='b; iP0'
            behaviour[1]='i;0rP1;1iP0,L; rP1'
            behaviour[2]='r; iL;*rR'
        elif choice==5:
            machinetitle='Petzold pp. 102-8, root of 2'
            numstates=27
            behaviour[0]='b; nP@,R,P1'
            behaviour[1]='n;@mR;*nL'
            behaviour[2]='m;0mR,Px,R;1mR,Px,R; xR,Pz,R,R,Pr'
            behaviour[3]='x;xrP ;@sN;*xL,L'
            behaviour[4]='r;rRR,R;*rR,R'
            behaviour[5]='R;rRR,R; xPr,R,R,Pr'
            behaviour[6]='s;@fR,R;*sL,L'
            behaviour[7]='f;xFL;yFL;zDL; fR,R'
            behaviour[8]='F;00R;1dR,R,R'
            behaviour[9]='d;xDL;yDL; dR,R'
            behaviour[10]='D;00R;11R; 1R'
            behaviour[11]='0;raPs;uaPv;*0R,R'
            behaviour[12]='1;raPv;ucPs,R,R;*1R,R'
            behaviour[13]='c;raPu; zPu;ucPr,R,R'
            behaviour[14]='a;@eR,R;*aL,L'
            behaviour[15]='e;xyP ,L,L;zyPy,L,L;*eR,R'
            behaviour[16]='y;@ER,R;ysPz; sPx'
            behaviour[17]='E;yYP ,L,L;*ER,R'
            behaviour[18]='Y;@oR;*XPy,R'
            behaviour[19]='X; uR,Px;*XR,R'
            behaviour[20]='u;sUPt,R,R;vUPw,R,R;*uR,R'
            behaviour[21]='U;sUPr,R,R;vUPu,R,R;*sN'
            behaviour[22]='z;@pR;*zL'
            behaviour[23]='p;0pR,P ,R;1pR,P ,R; CP0,R,R,R'
            behaviour[24]='o;@PR;*oL'
            behaviour[25]='P;0PR,P ,R;1PR,P ,R; CP1,R,R,R'
            behaviour[26]='C; nN;*CP ,R,R'

    def statestr(i):
        out=str(i)+" ('"+statecodes[i-1]+"')"
        return out

    def analysemachine():
        global statecodes
        global numstates
        result=True
        i=0
        while i<numstates:
            if behaviour[i]=='':
                for j in range(i+1,numstates):
                    behaviour[j-1]=behaviour[j]
                numstates-=1
            else:
                s=behaviour[i]
                statecodes=statecodes+s[0]
                posn=s.find(';')
                while posn>=0:
                    s=s[posn+1:]
                    if len(s)>1:
                        if triggerstring[i].find(s[0])>=0:
                            print('State '+statestr(i+1)+' has multiple actions for character "'+s[0]+'"')
                            result=False
                        triggerstring[i]=triggerstring[i]+s[0]
                        transitionstring[i]=transitionstring[i]+s[1]
                    posn=s.find(';')
                i+=1
        for i in range(numstates-1):
            for j in range(i+1,numstates):
                if statecodes[i]==statecodes[j]:
                    print('States '+str(i)+' and '+str(j)+' both have code "'+statecodes[i]+'".')
                    result=False
        if result:
            for i in range(numstates):
                for j in range(len(transitionstring[i])):
                    posn=statecodes.find(transitionstring[i][j])
                    if posn==-1:
                        print('Transition state code "'+transitionstring[i][j]+'" is not recognised.')
                        result=False
                    else:
                        transitionstring[i]=transitionstring[i][:j]+chr(posn+1)+transitionstring[i][j+1:]
        return result

    def getactstring(state,c):
        posn=behaviour[state].find(';'+c)
        if posn==-1:
            posn=behaviour[state].find(';*')
        if posn==-1:
            print('Inconsistent data or analysis for "'+c+'"in state '+statestr(state+1))
            result='HALT'
        else:
            result=behaviour[state][posn+3:] #check the logic
            posn=result.find(';')
            if posn>-1:
                x=True
                result=result[:posn] #check the logic
        return result

    def menu():
        blank(white)
        colour(brown)
        setxy(MARGIN,50)
        display('TURING MACHINE SIMULATOR',MENUTYPE|16,42)
        colour(darkred)
        setxy(MARGIN+30,175)
        display("(Examples are taken from Charles Petzold''s",MENUTYPE,30)
        setxy(MARGIN+30,225)
        display('excellent book, "The Annotated Turing")',MENUTYPE,30)
        colour(black)
        setxy(MARGIN,350)
        display('Choose from the following:',MENUTYPE|16,MENUSIZE)
        setxy(MARGIN,450)
        display('  1.  Petzold p. 81 (0 1 0 1 ...  4 states))',MENUTYPE,MENUSIZE)
        setxy(MARGIN,550)
        display('  2.  Petzold p. 84 (0 1 0 1 ...  1 state)',MENUTYPE,MENUSIZE)
        setxy(MARGIN,650)
        display('  3.  Petzold p. 87 (transcendental)',MENUTYPE,MENUSIZE)
        setxy(MARGIN,750)
        display('  4.  Petzold p. 99 (binary counting)',MENUTYPE,MENUSIZE)
        setxy(MARGIN,850)
        display('  5.  Petzold pp. 102-8, root of 2',MENUTYPE,MENUSIZE)
        detect("key", 0)
        choice=get_key_code()-48
        while (choice<=0) or (choice>=6):
            detect("key", 0)
            choice=get_key_code()-48
        definemachine(choice)
        blank(white)

    def dolabels():
        colour(red)
        setxy(MARGIN,TAPELABEL)
        display('TAPE:',FONTTYPE,FONTSIZE)
        setxy(MARGIN,CYCLELABEL)
        display('CYCLES:',FONTTYPE,FONTSIZE)
        setxy(MARGIN,TABLELABEL)
        display('MACHINE TABLE ('+machinetitle+'):',FONTTYPE,FONTSIZE)
        colour(lightgrey)
        setxy(400,CYCLELABEL)
        display('(press ESCAPE to return to menu)',FONTTYPE,FONTSIZE)

    def drawtable():

        def heading(s,width):
            colour(black)
            box(width,ROWHEIGHT+HEADSPACE*2,brown,True)
            colour(white)
            movexy(0,HEADSPACE+4)
            display(s,FONTTYPE|32,FONTSIZE)
            movexy(width,-HEADSPACE-4)

        def entry(s,width):
            box(width,ROWHEIGHT,white,True)
            movexy(0,4)
            display(s,FONTTYPE,FONTSIZE)
            movexy(width,-4)

        setxy(MARGIN,TABLETOP)
        heading(' m-config. ',150)
        heading(' symbol ',130)
        heading('              operations ',420)
        heading(' final m-config. ',230)
        colour(black)
        movexy(0,HEADSPACE*2)
        for i in range(numstates):
            for j in range(len(triggerstring[i])):
                setxy(MARGIN,turty()+ROWHEIGHT)
                if j==0:
                    entry('   '+statestr(i+1),150)
                else:
                    entry('',150)
                if triggerstring[i][j]==' ':
                    entry('   None',130)
                elif triggerstring[i][j]=='*':
                    entry('    Any',130)
                else:
                    entry('      '+triggerstring[i][j],130)
                entry(' '+getactstring(i,triggerstring[i][j]),420)
                entry('        '+statestr(ord(transitionstring[i][j])),230)

    def drawtape():
        global leftshown
        noupdate()
        setxy(0,TAPETOP-5)
        box(1000,2*cellwidth+10,white,False)
        if headpos<leftshown+SHOWLEFT:
            leftshown=headpos-SHOWLEFT
            if leftshown<leftmost-SHOWLEFTMIN:
                leftshown=leftmost-SHOWLEFTMIN
        elif headpos>=leftshown+SHOWCELLS-SHOWRIGHT:
            leftshown=headpos-SHOWCELLS+SHOWRIGHT+1
        setxy(lmargin-cellwidth,TAPETOP)
        for i in range(leftshown-1,leftshown+SHOWCELLS+1):
            box(cellwidth,cellwidth,cream,True)
            movexy(cmargin,0)
            display(tape[i],1,cellwidth/2)
            if i%5==0:
                movexy(-cmargin+2,-12)
                display('.',1,12)
                movexy(cmargin-2,12)
            movexy(cellwidth-cmargin,0)
        setxy(lmargin+cellwidth*(headpos-leftshown),TAPETOP)
        thickness(10)
        box(cellwidth,cellwidth,cyan,True)
        thickness(2)
        movexy(cmargin,0)
        display(tape[headpos],1,cellwidth/2)
        movexy(0,cellwidth+8)
        colour(brown)
        display(str(state+1),FONTTYPE,cellwidth/2)
        setxy(CYCLEINDENT,CYCLELABEL)
        box(200,100,white,False)
        display(str(cycles),FONTTYPE,cellwidth/2)
        colour(black)
        update()

    def dostep():
        global state
        global cycles
        global headpos
        global leftmost
        global rightmost

        def process(s):
            global headpos
            global leftmost
            global rightmost
            if s[0]=='L':
                headpos-=1
                if headpos<leftmost:
                    leftmost=headpos
            elif s[0]=='R':
                headpos+=1
                if headpos>rightmost:
                    rightmost=headpos
            elif s[0]=='P':
                if len(s)>1:
                    tape[headpos]=s[1]
                    if (s[1]=='0') or (s[1]=='1'):
                        print('Cycle = '+str(cycles)+'; Position = '+str(headpos)+'; State = '+statestr(state+1)+'; Printed = "'+s[1]+'"')
                else:
                    print('Null Print instruction for "'+thischar+'" in state '+statestr(state+1))
            posn=s.find(',')
            if posn==-1:
                s=''
            else:
                s=s[posn+1:]
            return s

        cycles+=1
        thischar=tape[headpos]
        if pausetime==200:
            print('Cycle = '+str(cycles)+'; Position = '+str(headpos)+'; State = '+statestr(state+1)+'; Symbol = "'+thischar+'"')
        posn=triggerstring[state].find(thischar)
        if posn==-1:
            posn=triggerstring[state].find('*')
        if posn==-1:
            print('Action for "'+thischar+'" is not defined for state '+statestr(state+1))
            halt()
        else:
            actstring=getactstring(state,thischar)
            if pausetime==200:
                print('Processing "'+actstring+'"')
            if actstring=='HALT':
                state=-1
            else:
                while actstring!='':
                    actstring=process(actstring)
                state=ord(transitionstring[state][posn])-1

    def showspeed():
        setxy(870,TAPELABEL)
        colour(brown)
        box(95,32,cream,True)
        if pausetime==200:
            display('SLOW',FONTTYPE,FONTSIZE)
        else:
            display(' FAST',FONTTYPE,FONTSIZE)

    headpos=100
    leftmost=100
    rightmost=100
    leftshown=headpos-SHOWLEFTMIN
    first=True
    while first or (state!=-1):
        first=False
        menu()
        if analysemachine():
            cycles=0
            dolabels()
            drawtable()
            drawtape()
            showspeed()
            state=0
            flag=True
            while flag or (get_key_sym()!="Escape"):
                flag=False
                dostep()
                drawtape()
                pause(pausetime)
                if (get_lmouse()>0) and (get_clickx()>870) and (get_clicky()<100):
                    pausetime=200-pausetime
                    showspeed()
                    update()
                    pause(500)
                    # Wait for mouse release
                    while get_lmouse()>0:
                        update()