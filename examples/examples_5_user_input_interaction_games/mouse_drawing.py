import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(800, 600) as t:

    def palette():
        for col in range(1,11,1):
            setxy(col*100-50,550)
            colour(rgb(col))
            blot(50)

    palette()
    home()
    thickness(10)
    blot(2)
    while True:
        pause(50)
        while not((get_lmouse()>0) or (get_rmouse()>0)):
            update()
        if get_mousey()>500:
            colour(rgb(get_mousex()//100+1))
        else:
            if get_lmouse()>0:
                drawxy(get_mousex()-turtx(),get_mousey()-turty())
            else:
                setxy(get_mousex(),get_mousey())
