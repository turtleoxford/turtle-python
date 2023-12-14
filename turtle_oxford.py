from contextlib import contextmanager
from logging import log
import math
from time import sleep
from tkinter import *


class TurtleCanvas:
    _direction = 0
    _angles = 360
    _x = 0
    _y = 0
    _thick = 1
    _colour = "black"
    _root = Tk()
    _canvas = None
    _home = 0, 0
    _pen = True

    def create(self, width=1000, height=1000):
        TurtleCanvas._root.title("Turtle")
        self._frame = Frame(self._root, width=width, height=height)
        self._frame.pack(expand=True, fill=BOTH)
        TurtleCanvas._canvas = Canvas(
            self._frame, bg="white", width=width, height=height
        )
        TurtleCanvas._canvas.pack(expand=True, fill=BOTH)
        TurtleCanvas._home = width / 2, height / 2
        TurtleCanvas._x, TurtleCanvas._y = TurtleCanvas._home

    def refresh():
        if not TurtleCanvas._canvas:
            log.error("Canvas not lanuched, please create a canvas first.")
        TurtleCanvas._root.update()


@contextmanager
def turtle_canvas(width=1000, height=1000):
    canvas = TurtleCanvas()
    try:
        canvas.create(width, height)
        yield canvas
    finally:
        TurtleCanvas._canvas.pack(expand=True, fill=BOTH)
        TurtleCanvas._canvas.mainloop()


def home():
    setxy(TurtleCanvas._home)


def setx(x):
    TurtleCanvas._x = x


def sety(y):
    TurtleCanvas._y = y


def setxy(x, y):
    TurtleCanvas._x = x
    TurtleCanvas._y = y


def colour(new_colour):
    TurtleCanvas._colour = new_colour


def thickness(new_thickness):
    TurtleCanvas._thick = new_thickness


def pause(duration):
    sleep(duration // 1000)
    TurtleCanvas.refresh()


def forward(distance):
    new_y = TurtleCanvas._y - distance * math.cos(math.radians(TurtleCanvas._direction))
    new_x = TurtleCanvas._x - distance * math.sin(math.radians(TurtleCanvas._direction))
    TurtleCanvas._canvas.create_line(
        TurtleCanvas._x,
        TurtleCanvas._y,
        new_x,
        new_y,
        fill=TurtleCanvas._colour,
        width=TurtleCanvas._thick,
    )
    TurtleCanvas._x = new_x
    TurtleCanvas._y = new_y


def right(degrees):
    TurtleCanvas._direction = (TurtleCanvas._direction - degrees) % 360

def blot(size):
    x1 = TurtleCanvas._x - size
    y1 = TurtleCanvas._y - size
    x2 = TurtleCanvas._x + size
    y2 = TurtleCanvas._y + size
    oval = TurtleCanvas._canvas.create_oval(x1, y1, x2, y2, fill=TurtleCanvas._colour, width=0)
