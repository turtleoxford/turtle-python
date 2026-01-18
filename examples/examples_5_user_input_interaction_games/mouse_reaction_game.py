import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    blank(cream)
    setxy(15,200)
    colour(black)
    display('This reaction game will display a sequence',4,36)
    setxy(20,270)
    display('of 10 coloured circles on the Canvas.  Try',4,36)
    setxy(20,340)
    display('to click the mouse on each circle as quickly',4,36)
    setxy(20,410)
    display('as you can, and see how short a total time',4,36)
    setxy(20,480)
    display('you can achieve for all 10.',4,36)
    setxy(100,620)
    display('Now press the "Esc" key to start ...',4,36)
    keyecho(False)
    while (abs(get_key_code())!=27):
        pause(100)
        pass
    timeset(0)
    for count in range(1,10,1):
        x=randint(50,600)
        y=randint(50,600)
        blank(black)
        setxy(x,y)
        target_colour = rgb(count)
        colour(target_colour)
        blot(50)
        clickcol = -1
        while clickcol!=target_colour:
            update()
            while status("mouse1")<=0:
                update()
            clickcol=pixcol(get_clickx(),get_clicky())
    blank(lightblue)
    setxy(60,460)
    colour(lightred)
    display('Your time was '+qstr(time(),1000,2)+' seconds',4,50)