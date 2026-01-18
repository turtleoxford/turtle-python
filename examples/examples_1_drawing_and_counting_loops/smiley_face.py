import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # avoid drawing lines as Turtle moves
    penup()
    # draw head
    colour(peach)
    blot(200)
    # draw mouth using overlapping blots
    colour(darkred)
    blot(140)
    forward(30)
    colour(peach)
    blot(150)
    # draw blue nose
    back(60)
    colour(royal)
    # move to left eye position
    blot(30)
    forward(90)
    left(90)
    # Turtle is now pointing leftwards
    forward(80)
    # draw left eye
    colour(white)
    ellblot(30,20)
    colour(emerald)
    blot(18)
    colour(black)
    blot(8)
    # move to right eye position
    back(160)
    # draw right eye
    colour(white)
    ellblot(30,20)
    colour(emerald)
    blot(18)
    colour(black)
    blot(8)