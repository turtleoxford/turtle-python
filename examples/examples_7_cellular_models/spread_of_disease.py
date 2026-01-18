import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    # Set up map dimensions and colours
    width=100
    height=100
    susceptible=lightgreen
    infected=red
    recovered=blue

    # Set up disease parameters
    startradius=10
    infectprob=1
    immuneprob=2
    recoverprob=15

    # Do cells move?  Should the numbers be continuously reported?
    movement=False
    report=False

    # Set up counters for numbers infected and infectious
    numinfected=0
    numinfectious=0

    # Function that infects cell (x,y)
    def infect(x,y):
        global numinfected, numinfectious
        pixset(x,y,infected)
        numinfected+=1
        numinfectious+=1
        if report:
            print('Infected: '+pad(str(numinfected),' ',4)+'      Infectious: '+pad(str(numinfectious),' ',4))

    # Main program: set up Canvas and timer, and initialise counts        
    canvas(0,0,width,height)
    timeset(0)
    numimmune=0
    numinfected=0
    numinfectious=0

    # Set initial infection around the centre of the Canvas
    noupdate()
    for x in range(width):
        for y in range(height):
            if (randrange(100)<infectprob) and (hypot(x-width/2,y-height/2)<=startradius):
                infect(x,y)
            elif randrange(100)<immuneprob:
                pixset(x,y,recovered)
                numimmune+=1
            else:
                pixset(x,y,susceptible)
    update()

    #Main loop while any infection persists
    while numinfectious>0:

        #Pick a random cell
        x=randrange(width)
        y=randrange(height)

        # If it's infected, it may recover
        if pixcol(x,y)==infected:
            if randrange(100)<recoverprob:
                pixset(x,y,recovered)
                numinfectious-=1
                if report:
                    print('                    Infectious: '+pad(str(numinfectious),' ',4))

            # But otherwise, it may infect an adjacent cell
            else:
                n=randrange(4)*2+1
                x=x+n//3-1
                y=y+n%3-1
                if pixcol(x,y)==susceptible:
                    infect(x,y)

        # If movement is enabled, pick a random cell and if not susceptible, swap it 
        if movement:
            x=randrange(width)
            y=randrange(height)
            if pixcol(x,y)!=susceptible:
                x2=randrange(width)
                y2=randrange(height)
                swapcol=pixcol(x,y)
                pixset(x,y,pixcol(x2,y2))
                pixset(x2,y2,swapcol)

    # When all infection has died down, display the overall figures and timing 
    print('Total infected overall: '+str(numinfected)+' ('+qstr(time(),1000,2)+' sec)')
    print('Proportion infected:    '+qstr(numinfected*100,width*height-numimmune,2)+'%')