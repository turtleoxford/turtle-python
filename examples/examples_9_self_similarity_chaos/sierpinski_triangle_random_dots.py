import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    x=[400,843,179]
    y=[138,650,778]
    thisx=randint(400,600)
    thisy=randint(400,600)
    while True:
        thisc=randrange(3)
        thisx=(thisx+x[thisc])/2
        thisy=(thisy+y[thisc])/2
        pixset(thisx,thisy,purple)