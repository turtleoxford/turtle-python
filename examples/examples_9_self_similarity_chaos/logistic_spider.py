import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    # Setup constants
    maxpop=100000   # Maximum population
    maxgen=100      # Maximum generation range
    lmargin=60      # Margins around graph
    rmargin=40
    tmargin=150
    bmargin=200
    showoutput=True # Show population figures?

    # Draw graph axes and caption
    def axes():
        colour(black)
        for i in range(11):
            setxy(i*100-25,1000)
            display(qstr(i,10,1),4,20) # label horizontal axis
        for i in range(1,11):
            setxy(-lmargin+5,1000-i*100-20)
            display(qstr(i,10,1),4,20) # label vertical axis
        setxy(0,0)
        drawxy(0,1000) # draw vertical axis
        drawxy(1000,0) # draw horizontal axis
        colour(red)
        setxy(0,1060) # position to display graph caption
        display('Population over '+str(maxgen)+' generations, where P (population/'+str(maxpop)+')',4,25)
        setxy(0,1110)
        display('is determined by the logistic equation P\' = rP(1 - P), with r = '+qstr(r,10,1),4,25)

    # Draw menu of r values from 2.1 to 4.0
    def menu():
        colour(black)
        setxy(10,-tmargin+20)
        display('Set r:',4,25)
        for i in range(21,41):
            setxy(((i-1)%10)*90+130,((i-1)//10)*50-100-tmargin)
            if (i==r):
                box(90,50,red,True) # show actual r value (e.g. 25 or 30) in red box
            else:
                box(90,50,cream,True)
            display('  '+qstr(i,10,1),4,25)

    # Plot y=x line, and curve of chosen logistic equation
    def curve():
        noupdate()
        colour(black)
        setxy(0,1000)
        drawxy(1000,-1000) # draw black y=x line
        colour(blue)
        setxy(0,1000)
        for i in range(1,101):
            popx=divmult(i,100,maxpop) # Set popx to 1%, 2%, ... 100% of maxpop
            popy=divmult(popx,10*maxpop,r*(maxpop-popx)) # Calculate y-value of graph
            setxy(divmult(popx,maxpop,1000),1000-divmult(popy,maxpop,1000))
            polyline(2) # draw next segment of graph curve
        update()

    # Main program: setup canvas and loop
    canvas(-lmargin,-tmargin,1000+lmargin+rmargin,1000+tmargin+bmargin)
    thickness(3)
    r=25
    while True:
        noupdate()
        blank(white)
        axes()  # Canvas is set up so top left of graph is at (0,0)
        menu()  # redraw menu of r values, highlighting the current value in red
        curve() # draw y=x and the logistic equation curve
        pop=randint(10,maxpop) # start with a random population, minimum 10
        if showoutput:
            print()
            print('r = '+qstr(r,10,1)+' Initial population = '+str(pop))
        setxy(divmult(pop,maxpop,1000),1000) # move Turtle to corresponding point on x-axis
        for gen in range(1,maxgen+1):
            colour(mixcols(lightgreen,green,maxgen-gen,gen)) # darken from lightgreen to green
            pop=divmult(pop,10*maxpop,r*(maxpop-pop)) # apply equation to give next population
            drawxy(0,1000-divmult(pop,maxpop,1000)-turty()) # draw vertical line to hit curve
            drawxy(divmult(pop,maxpop,1000)-turtx(),0) # draw horizontal line to hit y=x
            if showoutput:
                print(str(pop), end=" ")
                if (gen%10==0):
                    print()
        blot(3)
        update()
        while not((get_lmouse()>0) and (get_clicky()<(100-tmargin)) and (get_clickx()>=130) and (get_clickx()<1030)):
            pause(50)
        r=((get_clickx()-130)//90)+((get_clicky()+tmargin+100)//50)*10+1