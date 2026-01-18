import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    width=100
    height=100
    susceptible=lightgreen
    infectious=red
    recovered=blue
    initialnumber=10
    infectprob=2
    contacts=50
    numinfected=0
    numinfectious=0

    # function to infect cell at (x,y) - assumes that it is susceptible
    def infect(x,y):
        global numinfected, numinfectious
        pixset(x,y,infectious)
        numinfected+=1
        numinfectious+=1

    # set up canvas, with all cells initially susceptible
    canvas(0,0,width,height)
    blank(susceptible)

    # write out the general parameters of the model
    print('Initial infections:        '+str(initialnumber))
    print('Contacts per person:       '+str(contacts))
    print('Transmission probability:  '+str(infectprob)+'%')
    print('R0 (reproduction number):  '+qstr(contacts*infectprob,100,2))

    # initialise the counts
    numinfected=0
    numinfectious=0

    # randomly select the initial infections
    while numinfected<initialnumber:
        i=randrange(width)
        j=randrange(height)
        if pixcol(i,j)==susceptible:
            infect(i,j)

    # now run and time the model until nobody is still infectious
    timeset(0)
    while numinfectious>0:
        # randomly choose an individual
        x=randrange(width)
        y=randrange(height)
        # if that individual is infectious
        if pixcol(x,y)==infectious:
            # count through their contacts
            for n in range(contacts):
                # randomly choose whether the disease could be passed on in this case ...
                if randrange(100)<infectprob:
                    # if so, and the contact turns out to be susceptible, then they catch it
                    i=randrange(width)
                    j=randrange(height)
                    if pixcol(i,j)==susceptible:
                        infect(i,j)
            # the individual now recovers and becomes immune
            pixset(x,y,recovered)
            numinfectious-=1

    # when nobody remains infectious, report results
    print('Total infected overall:    '+str(numinfected)+' ('+qstr(time(),1000,2)+' sec)')
    print('Proportion infected:       '+qstr(numinfected*100,width*height,2)+'%')