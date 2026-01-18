"""
Turtle Oxford Plus - a python library for the Oxford Turtle System with extended features
"""

from contextlib import contextmanager
import logging
import math
import os
import shutil
from PIL import ImageColor
from time import sleep
from tkinter import *
from typing import (TypeAlias, IO)
from constants import *
import random
import string
import sys
from datetime import datetime
import glob
import datetime as dt

class Turtle:
    """Represents a turtle's state.
    """
    def __init__(self, x = 0, y = 0, direction = 0, colour = "black", thick = 1, layer = 0, **kwargs):
        self.x = x
        self.y = y
        self.direction = direction
        self.colour = colour
        self.thick = thick
        self.layer = layer
        self.parameters = {k: v for k, v in kwargs.items()}

    def __repr__(self):
        return f"Turtle(x={self.x}, y={self.y}, direction={self.direction}, colour={self.colour}, thick={self.thick}, layer={self.layer})"
    
    @property
    def params(self):
        return self.parameters
    
    @params.setter
    def params(self, value):
        self.parameters = value

class TurtleCanvasClass:
    """Singleton Class describing the turtle and the canvas.
    """
    def __init__(self):
        # Turtle vars
        self._history: list[tuple[int, int]] = []
        self._turtles: list[Turtle] = [Turtle()]
        self._current_turtle_index: int = 0
        self._time: int = datetime.now()
        self._layers: list[int] = [0]
        self._angles: int = 360 # Change to turtle attribute
        # Canvas vars
        self._root: Tk | None = None
        self._canvas: Canvas | None = None
        self._home: tuple[int, int] = 0, 0
        self._origin_x: int = 0
        self._origin_y: int = 0
        self._pen: bool = True
        self._update: bool = True
        self._x_multiplier: float = 1
        self._y_multiplier: float = 1
        self._width: int = 0
        self._height: int = 0
        # Input vars
        self._key_code: int = 0
        self._key_sym: str = ""
        self._kshift: int = 128
        # Possible values: +kshift, -kshift (pressed and released respectively)
        self._pressed_keys: dict[str, int] = {}
        self._mousex: int = -1
        self._mousey: int = -1
        # Search vars
        self._dir_search_results: list[str] = []
        self._file_search_results: list[str] = []
        # Key buffer vars
        self._key_buffer: list = []
        self._key_buffer_size: int = 0
        self._key_echo: bool = False

    @property
    def _current_turtle(self) -> Turtle:
        """
        Get the current turtle.
        """
        return self._turtles[self._current_turtle_index]

    @property
    def _x(self) -> int:
        return self._turtles[self._current_turtle_index].x

    @_x.setter
    def _x(self, value: int):
        self._turtles[self._current_turtle_index].x = value

    @property
    def _y(self) -> int:
        return self._turtles[self._current_turtle_index].y

    @_y.setter
    def _y(self, value: int):
        self._turtles[self._current_turtle_index].y = value

    @property
    def _direction(self) -> int:
        return self._turtles[self._current_turtle_index].direction

    @_direction.setter
    def _direction(self, value: int):
        self._turtles[self._current_turtle_index].direction = value

    @property
    def _thick(self) -> int:
        return self._turtles[self._current_turtle_index].thick

    @_thick.setter
    def _thick(self, value: int):
        self._turtles[self._current_turtle_index].thick = value

    @property
    def _colour(self) -> str:
        return self._turtles[self._current_turtle_index].colour

    @_colour.setter
    def _colour(self, value: str):
        self._turtles[self._current_turtle_index].colour = value

    @property
    def _layer(self) -> int:
        return self._turtles[self._current_turtle_index].layer

    @_layer.setter
    def _layer(self, value: int):
        self._turtles[self._current_turtle_index].layer = value

    def create(
        self,
        width: int = 500,
        height: int = 500,
    ):
        """
        Create a new canvas with a new Turtle.

        :param origin_x: the x coordinate of the origin of the canvas (Default: 0)
        :type origin_x: int
        :param origin_y: the y coordinate of the origin of the canvas (Default: 0)
        :type origin_y: int
        :param width: the width of the canvas (Default: 500)
        :type width: int
        :param height: the height of the canvas (Default: 500)
        :type height: int
        """
        self._width = width
        self._height = height
        self._root = Tk()
        self._root.title("Turtle")

        self._frame = Frame(
            self._root, width=self._width, height=self._height + 100
        )
        self._frame.pack(expand=True, fill=BOTH)
        self._halt = Button(self._frame, text="HALT")
        self._halt.pack()

        self._canvas = Canvas(
            self._frame, bg="white", width=width, height=height
        )
        self._canvas.pack(side="bottom")
        self._canvas.focus_set()
        self._canvas.bind("<KeyPress>", on_press)
        self._canvas.bind("<KeyRelease>", on_release)
        self._canvas.bind("<ButtonPress>", on_press)
        self._canvas.bind("<ButtonRelease>", on_release)

        self._halt.bind("<ButtonRelease>", halt)

        self._origin_x, self._origin_y = 0, 0
        self._home = width / 2, height / 2
        self._x, self._y = self._home

    def refresh(self):
        """
        Refresh the canvas to display the latest drawings.
        """
        if not self._canvas:
            logging.error("Canvas not lanuched, please create a canvas first.")
        self._root.update()

TurtleCanvas = TurtleCanvasClass()

def _scale_x(x: int) -> float:
    """
    Helper function. Scales the x coordinate to the canvas resolution.

    :param x: the x coordinate to be scaled
    :type x: int
    :return: the scaled x coordinate
    :rtype: float
    """

    return (x - TurtleCanvas._origin_x) * TurtleCanvas._x_multiplier

def _scale_y(y: int) -> float:
    """
    Helper function. Scales the y coordinate to the canvas resolution.

    :param y: the y coordinate to be scaled
    :type y: int

    :return: the scaled y coordinate
    :rtype: float
    """

    return (y - TurtleCanvas._origin_y) * TurtleCanvas._y_multiplier

def _degs_to_angle_units(degs: int) -> int:
    """
    Helper function. Converts degrees to angle units.

    :param degs: the number of degrees to convert
    :type degs: int
    :return: the number of angle units
    :rtype: int
    """

    return degs * TurtleCanvas._angles / 360


@contextmanager
def turtle_canvas(width: int = 500, height: int = 500):
    """
    Context manager that creates a canvas at the start and halts at the end.

    :param origin_x: the x coordinate of the origin of the canvas (Default: 0)
    :type origin_x: int
    :param origin_y: the y coordinate of the origin of the canvas (Default: 0)
    :type origin_y: int
    :param width: the width of the canvas (Default: 500)
    :type width: int
    :param height: the height of the canvas (Default: 500)
    :type height: int
    """
    try:
        TurtleCanvas.create(width, height)
        yield TurtleCanvas
    except TclError:
        logging.debug("Window closed")
    finally:
        TurtleCanvas._canvas.mainloop()


def update():
    """
    Update the Canvas, and continue updating with all subsequent drawing commands.
    """
    TurtleCanvas._update = True
    TurtleCanvas.refresh()


def noupdate():
    """
    Refrain from updating the Canvas when executing all subsequent drawing commands, until update() is called.
    """
    TurtleCanvas._update = False


def canvas(x_origin: int, y_origin:int, x: int, y: int):
    """ Set the resolution of the canvas to x by y
    :param x_origin: x coordinate of the top left corner
    :type x_origin: int
    :param y_origin: y coordinate of the top left corner
    :type x_origin: int
    :param x: resolution on the x axis
    :type x: int
    :param y: resolution on the y axis
    :type y: int
    """
    TurtleCanvas._x_multiplier = TurtleCanvas._width / x
    TurtleCanvas._y_multiplier = TurtleCanvas._height / y
    TurtleCanvas._canvas.scale(
        "all",
        0,
        0,
        TurtleCanvas._x_multiplier,
        TurtleCanvas._y_multiplier,
    )
    TurtleCanvas._home = x/2, y/2
    TurtleCanvas._x /= TurtleCanvas._x_multiplier
    TurtleCanvas._y /= TurtleCanvas._y_multiplier
    TurtleCanvas._origin_x = x_origin
    TurtleCanvas._origin_y = y_origin


def move(func: callable) -> callable:
    """Private. Decorator for movement functions.

    :param func: name of a movement function
    :type func: callable
    :return: modified function with the boilerplate added
    :rtype: callable
    """
    def inner(*args, **kwargs):
        val = func(*args, **kwargs)
        TurtleCanvas._history.append((TurtleCanvas._x, TurtleCanvas._y))
        return val

    return inner


def remember():
    """
    Add the current coordinates to the history of the turtle
    """
    TurtleCanvas._history.append((TurtleCanvas._x, TurtleCanvas._y))


def forget(n: int):
    """
    Forget the last n positions of the turtle

    :param n: number of positions to forget
    :type n: int
    """
    for i in range(n):
        TurtleCanvas._history.pop()


# Change coordinates
def home():
    """
    Move the turtle to the center of the canvas
    """
    setxy(*TurtleCanvas._home)


@move
def setx(x: int):
    """Set the x coordinate

    :param x: the new x coordinate of the turtle
    :type x: int
    """
    TurtleCanvas._x = x


@move
def sety(y: int):
    """Set the y coordinate

    :param y: the new y coordinate of the turtle
    :type y: int
    """
    TurtleCanvas._y = y


@move
def setxy(x: int, y: int):
    """Set both coordinates

    :param x: the new x coordinate of the turtle
    :type x: int
    :param y: the new y coordinate of the turtle
    :type y: int
    """
    TurtleCanvas._x = x
    TurtleCanvas._y = y


# Change colour


def colour_to_int(colour: tuple[int, int, int] | int | str) -> int:
    """Convert the colour parameter from any acceptable format to an integer (from 0 to 255).

    :param colour: colour to be converted
    :type colour: tuple[int, int, int] | int | str
    :return: the integer format of the colour
    :rtype: int
    """
    if isinstance(colour, int):
        return colour
    elif isinstance(colour, str):
        return colour_to_int(ImageColor.getrgb(colour))
    elif isinstance(colour, tuple):
        r, g, b = colour
        return (r << 16) + (g << 8) + b


def colour_to_str(colour: tuple[int, int, int] | int | str) -> str:
    """Convert the colour parameter form any acceptable format to a string.

    :param colour: colour to be converted
    :type colour: tuple[int, int, int] | int | str
    :return: the string format of the colour
    :rtype: str
    """
    if isinstance(colour, str):
        return colour
    elif isinstance(colour, tuple):
        r, g, b = colour
        # hex strings start with 0x so we strip that to create the colour hex
        return f"#{hex(r)[2:]}{hex(g)[2:]}{hex(b)[2:]}"
    elif isinstance(colour, int):
        return f"#{colour.to_bytes(3, 'big').hex()}"


def colour(new_colour: tuple[int, int, int] | int | str):
    """Set the new colour of the turtle.

    :param new_colour: new colour, as either an (r, g, b) tuple, a rgb hex integer or a string
    :type new_colour: tuple[int, int, int] | int | str
    """
    TurtleCanvas._colour = colour_to_str(new_colour)


# Change pen


def thickness(new_thickness: int):
    """Set the thickness of the pen

    :param new_thickness: new thickness of the pen.
    :type new_thickness: int
    """
    TurtleCanvas._thick = new_thickness


def set_layer(layer: int):
    """Sets the turtle's drawing layer.

    :param layer: The layer to draw on.
    :type layer: int
    """
    TurtleCanvas._layer = layer
    if layer not in TurtleCanvas._layers:
        TurtleCanvas._layers.append(layer)
        TurtleCanvas._layers.sort()

def delete_layer(layer: int):
    """Deletes all drawings on a specific layer.

    :param layer: The layer to delete.
    :type layer: int
    """
    if layer in TurtleCanvas._layers:
        TurtleCanvas._canvas.delete(f"layer{layer}")
        TurtleCanvas._layers.remove(layer)
        if TurtleCanvas._layer == layer:
            TurtleCanvas._layer = 0
            if 0 not in TurtleCanvas._layers:
                TurtleCanvas._layers.append(0)
                TurtleCanvas._layers.sort()

def change_layer_index(old_index: int, new_index: int):
    """Changes the index of a specific layer.

    :param old_index: The current index of the layer.
    :type old_index: int
    :param new_index: The new index of the layer.
    :type new_index: int
    """
    if old_index in TurtleCanvas._layers:
        TurtleCanvas._canvas.itemconfig(f"layer{old_index}", tags=f"layer{new_index}")
        TurtleCanvas._layers.remove(old_index)
        if new_index not in TurtleCanvas._layers:
            TurtleCanvas._layers.append(new_index)
            TurtleCanvas._layers.sort()
        if TurtleCanvas._layer == old_index:
            TurtleCanvas._layer = new_index

def switch_layers(index1: int, index2: int):
    """Switches the indices of two layers.

    :param index1: The index of the first layer.
    :type index1: int
    :param index2: The index of the second layer.
    :type index2: int
    """
    if index1 in TurtleCanvas._layers and index2 in TurtleCanvas._layers:
        TurtleCanvas._canvas.itemconfig(f"layer{index1}", tags="temp_layer")
        TurtleCanvas._canvas.itemconfig(f"layer{index2}", tags=f"layer{index1}")
        TurtleCanvas._canvas.itemconfig("temp_layer", tags=f"layer{index2}")
        if TurtleCanvas._layer == index1:
            TurtleCanvas._layer = index2
        elif TurtleCanvas._layer == index2:
            TurtleCanvas._layer = index1

def penup():
    """Pick up the pen, stop drawing.
    """
    TurtleCanvas._pen = False


def pendown():
    """Put down the pen, all movement functions now produce drawings.
    """
    TurtleCanvas._pen = True


def pause(duration: int):
    """Pause `duration` milliseconds.

    :param duration: number milliseconds to pause
    :type duration: int
    """
    sleep(duration / 1000)
    TurtleCanvas.refresh()


# Change direction


def right(degrees: int):
    """Turn right.

    :param degrees: number of degrees to turn right
    :type degrees: int
    """
    TurtleCanvas._direction = (TurtleCanvas._direction - _degs_to_angle_units(degrees)) % 360


def left(degrees: int):
    """Turn left.

    :param degrees: number of degrees to turn left
    :type degrees: int
    """
    TurtleCanvas._direction = (TurtleCanvas._direction + _degs_to_angle_units(degrees)) % 360


def direction(degrees: int):
    """Turtle changes direction to face this number of degrees.

    :param degrees: number of degrees that indicate a direction to face
    :type degrees: int
    """
    TurtleCanvas._direction = _degs_to_angle_units(degrees)


# There is little actual support for the custom angles
def angles(degrees: int):
    """Change the number of degrees in a circle.

    :param degrees: number of degrees in a circle
    :type degrees: int
    """
    TurtleCanvas._angles = degrees


def turnxy(x: int, y: int):
    """Turn to face the point (x, y) on the canvas.

    :param x: the x coordinate of the point to face
    :type x: int
    :param y: the y coordinate of the point to face
    :type y: int
    """
    # if y/x = tan t, then t = arctan(y/x)
    TurtleCanvas._direction = math.degrees(math.atan(y / x))


# Draw shapes

# Define a decorator for the drawing functions which handles the drawing boilerplate
def draw(func: callable) -> callable:
    """Private. A decorator for the drawing functions.

    :param func: the name of a drawing function
    :type func: callable
    :return: the drawing function with the boilerplate added
    :rtype: callable
    """
    def inner(*args, **kwargs) -> int:
        id: int = func(*args, **kwargs)
        for layer in TurtleCanvas._layers:
            TurtleCanvas._canvas.tag_raise(f"layer{layer}")
        if TurtleCanvas._update:
            TurtleCanvas.refresh()
        TurtleCanvas._canvas.focus_set()
        return id

    return inner


def forward(distance: int) -> int:
    """Move forward.
    :param distance: distance to travel forward.
    :type distance: int
    :return: id of the shape drawn, if the pen is down, else -1.
    :rtype: int
    """
    return movexy(
        -distance * math.sin(math.radians(TurtleCanvas._direction)),
        -distance * math.cos(math.radians(TurtleCanvas._direction)),
    )


def back(distance: int) -> int:
    """Move back.
    :param distance: distance to travel back.
    :type distance: int
    :return: id of the shape drawn, if the pen is down, else -1.
    :rtype: int
    """
    return forward(-distance)


@move
def movexy(x: int, y: int) -> int:
    """Move to point (x, y).

    :param x: x coordinate of the destination point
    :type x: int
    :param y: y coordinate of the destination point
    :type y: int
    :return: id of the shape drawn, if the pen is down, else -1
    :rtype: int
    """
    new_x = TurtleCanvas._x + x
    new_y = TurtleCanvas._y + y
    if TurtleCanvas._pen:
        id = _draw_line(TurtleCanvas._x, TurtleCanvas._y, new_x, new_y)
    else:
        id = -1
    TurtleCanvas._x = new_x
    TurtleCanvas._y = new_y
    return id


@move
def drawxy(x: int, y: int) -> int:
    """Move to point (x, y), drawing a line regadless of the pen position.
    :param x: x coordinate of the destination point
    :type x: int
    :param y: y coordinate of the destination point
    :type y: int
    :return: id of the shape drawn
    :rtype: int
    """
    new_x = TurtleCanvas._x + x
    new_y = TurtleCanvas._y + y
    id = _draw_line(TurtleCanvas._x, TurtleCanvas._y, new_x, new_y)
    TurtleCanvas._x = new_x
    TurtleCanvas._y = new_y
    return id


@draw
def _draw_line(x: int, y: int, new_x: int, new_y: int):
    """Private. Helper class used to draw a line between two points.
    """
    return TurtleCanvas._canvas.create_line(
        _scale_x(x),
        _scale_y(y),
        _scale_x(new_x),
        _scale_y(new_y),
        fill=TurtleCanvas._colour,
        width=TurtleCanvas._thick * TurtleCanvas._x_multiplier,
        tags=f"layer{TurtleCanvas._layer}",
    )


@draw
def blot(size: int) -> int:
    """Draw a filled circle.

    :param size: radius of the circle
    :type size: int
    :return: the id of the shape drawn
    :rtype: int
    """
    return _oval(size, size, fill=True)


@draw
def circle(size: int) -> int:
    """Draw the outline of a circle.

    :param size: radius of the circle
    :type size: int
    :return: the id of the shape drawn
    :rtype: int
    """
    return _oval(size, size, border=True)


@draw
def ellipse(xradius: int, yradius: int) -> int:
    """Draw the outline of an ellipse.

    :param xradius: radius of the ellipse on the x coordinate
    :type xradius: int
    :param yradius: radius of the ellipse on the y coordinate
    :type yradius: int
    :return: id of the shape drawn
    :rtype: int
    """
    return _oval(xradius, yradius, border=True)


@draw
def ellblot(xradius: int, yradius: int) -> int:
    """Draw a filled ellipse.

    :param xradius: _description_
    :type xradius: int
    :param yradius: _description_
    :type yradius: int
    :return: _description_
    :rtype: int
    """
    return _oval(xradius, yradius, fill=True)


@draw
def _oval(xradius: int, yradius: int, border: bool = False, fill: bool = False) -> int:
    """Private. Helper function for drawing elliptical shapes.
    """
    x1 = _scale_x(TurtleCanvas._x - xradius)
    y1 = _scale_y(TurtleCanvas._y - yradius)
    x2 = _scale_x(TurtleCanvas._x + xradius)
    y2 = _scale_y(TurtleCanvas._y + yradius)
    id = -1
    if border:
        id = TurtleCanvas._canvas.create_oval(
            x1,
            y1,
            x2,
            y2,
            width=TurtleCanvas._thick * TurtleCanvas._x_multiplier,
            outline=TurtleCanvas._colour,
            tags=f"layer{TurtleCanvas._layer}",
        )
    if fill:
        id = TurtleCanvas._canvas.create_oval(
            x1, y1, x2, y2, width=0, fill=TurtleCanvas._colour, tags=f"layer{TurtleCanvas._layer}"
        )
    return id


@draw
def pixset(x: int, y: int, colour: int) -> int:
    """Set the colour of the pixel at the (x, y) coordinates.

    :param x: the x coordinate of the pixel
    :type x: int
    :param y: the y coordinate of the pixel
    :type y: int
    :param colour: the new colour of the pixel 
    :type colour: int
    :return: the id of the pixel
    :rtype: int
    """
    return TurtleCanvas._canvas.create_rectangle(
        _scale_x(x),
        _scale_y(y),
        _scale_x(x + 1),
        _scale_y(y + 1),
        fill=colour_to_str(colour),
        width=0,
        tags=f"layer{TurtleCanvas._layer}",
    )


@draw
def box(x: int, y: int, colour: int, border: bool) -> int:
    """Draw a rectangle.

    :param x: the width of the rectangle
    :type x: int
    :param y: the height of the rectangle
    :type y: int
    :param colour: the colour of the inside of the rectangle
    :type colour: int
    :param border: true if the rectangle should have a border
    :type border: bool
    :return: id of the shape drawn
    :rtype: int
    """
    return TurtleCanvas._canvas.create_rectangle(
        _scale_x(TurtleCanvas._x),
        _scale_y(TurtleCanvas._y),
        _scale_x(TurtleCanvas._x + x),
        _scale_y(TurtleCanvas._y + y),
        fill=colour_to_str(colour),
        width=int(border) * TurtleCanvas._thick,
        tags=f"layer{TurtleCanvas._layer}",
    )


@draw
def polyline(n: int):
    """Draw a sequence of lines connecting the last n points the turtle has visited.

    :param n: the number of points to consider
    :type n: int
    """
    x, y = TurtleCanvas._x, TurtleCanvas._y
    for (old_x, old_y) in TurtleCanvas._history[-n:]:
        id = _draw_line(x, y, old_x, old_y)
        x, y = old_x, old_y
    return id


@draw
def polygon(n: int):
    """Draw a polygon using the last n points the turtle has visited.

    :param n: the number of points in the polygon
    :type n: int
    """
    adjusted_points = [(_scale_x(x), _scale_y(y)) for (x, y) in TurtleCanvas._history[-n:]]
    return TurtleCanvas._canvas.create_polygon(
        *adjusted_points, fill=colour_to_str(TurtleCanvas._colour), tags=f"layer{TurtleCanvas._layer}"
    )


@draw
def display(text: str, font: str = "Helvetica", size: int = 12) -> int:
    """Display the text on the canvas.

    :param text: text to be displyed
    :type text: str
    :param font: font of the text, defaults to "Helvetica"
    :type font: str, optional
    :param size: font size, defaults to 12
    :type size: int, optional
    :return: id of the shape of the text
    :rtype: int
    """
    font_size = size * TurtleCanvas._x_multiplier
    t = TurtleCanvas._canvas.create_text(
        _scale_x(TurtleCanvas._x),
        _scale_y(TurtleCanvas._y),
        anchor="nw",
        font=(font, int(font_size)),
        fill=TurtleCanvas._colour,
        text=text,
        tags=f"layer{TurtleCanvas._layer}",
    )
    return t


@draw
def blank(colour) -> int:
    """Fill the canvas with a new colour.

    :param colour: new colour of the canvas
    :type colour: string or int
    :return: id of the shape of the canvas
    :rtype: int
    """
    r = TurtleCanvas._canvas.create_rectangle(
        0,
        0,
        TurtleCanvas._width,
        TurtleCanvas._height,
        fill=colour_to_str(colour),
        width=0,
        tags=f"layer{TurtleCanvas._layer}",
    )
    return r


@draw
# If boundary is a negative number, then any colour is acceptable
def fill(x: int, y: int, boundary: int | str):
    """Fill the area of the canvas with the current colour.

    :param x: x coordinate of the starting point
    :type x: int
    :param y: y coordinate of the starting point
    :type y: int
    :param boundary: colour of the border of the area to be filled
    :type boundary: int | str
    """
    if isinstance(boundary, str):
        boundary = colour_to_int(boundary)
    initcol = pixcol(x, y)

# get information about the canvas
def pixcol(x: int, y: int) -> int:
    ids = TurtleCanvas._canvas.find_overlapping(
        _scale_x(x),
        _scale_y(y),
        _scale_x(x + 1),
        _scale_y(y + 1),
    )
    if len(ids) == 0:
        # if no objects overlap, the pixel is white
        return white
    for id in reversed(ids):
        colour = TurtleCanvas._canvas.itemcget(id, "fill")
        if colour:
            return colour_to_int(colour)
    # All items overlapping the pixel are transparent
    return white


def get_key_sym() -> str:
    return TurtleCanvas._key_sym


def get_key_code() -> int:
    return TurtleCanvas._key_code


# user interactions

def on_press(event: Event):
    """Handle key and mouse press events.
    
    Updates the internal state of the keyboard and mouse based on the event.
    Records key symbols in the key buffer if it is enabled.
    
    :param event: the event triggered by a key or mouse press
    :type event: Event
    """
    TurtleCanvas._kshift = 128
    if event.keysym.startswith("Shift"):
        TurtleCanvas._kshift += 8
    elif event.keysym.startswith("Alt"):
        TurtleCanvas._kshift += 16
    elif event.keysym.startswith("Control"):
        TurtleCanvas._kshift += 32

    if event.type == EventType.Key:
        TurtleCanvas._key_code = event.keycode
        # This preserves the case for letters and removes the _L and _R from modifiers keys
        TurtleCanvas._key_sym = event.keysym.split("_")[0]
        TurtleCanvas._pressed_keys["key"] = TurtleCanvas._kshift
    else:
        TurtleCanvas._key_sym = "mouse" + str(event.num)
        TurtleCanvas._key_code = 128 + event.num
        TurtleCanvas._pressed_keys["mouse"] = TurtleCanvas._kshift
        TurtleCanvas._pressed_keys["clickx"] = event.x_root
        TurtleCanvas._pressed_keys["clicky"] = event.y_root
        TurtleCanvas._pressed_keys["click"] = TurtleCanvas._key_sym
    TurtleCanvas._pressed_keys[TurtleCanvas._key_sym] = TurtleCanvas._kshift
    TurtleCanvas._pressed_keys["mousekey"] = TurtleCanvas._kshift

    # Automatically add key presses to the buffer if key echo is enabled.
    if len(TurtleCanvas._key_buffer) < TurtleCanvas._key_buffer_size:
        TurtleCanvas._key_buffer.append(TurtleCanvas._key_sym)
    else:
        if TurtleCanvas._key_buffer:
            TurtleCanvas._key_buffer.pop(0)
            TurtleCanvas._key_buffer.append(TurtleCanvas._key_sym)
    if TurtleCanvas._key_echo:
        print(TurtleCanvas._key_sym, end="")

def on_release(event: Event):
    """Handle key and mouse release events.
    
    Updates the internal state to reflect released keys and mouse buttons.
    Changes the status flags for the released buttons or keys.
    
    :param event: the event triggered by a key or mouse release
    :type event: Event
    """
    if event.type == EventType.KeyRelease:
        TurtleCanvas._key_code = -event.keycode
        keysym = event.keysym.split("_")[0]
        TurtleCanvas._pressed_keys[keysym] *= -1
        TurtleCanvas._kshift *= -1
        TurtleCanvas._pressed_keys["key"] *= -1
    else:
        keysym = "mouse" + str(event.num)
        TurtleCanvas._pressed_keys[keysym] *= -1
        TurtleCanvas._pressed_keys["mouse"] *= -1
        TurtleCanvas._pressed_keys["click"] *= -1
    TurtleCanvas._pressed_keys["mousekey"] *= -1

def detect(key_sym, timeout) -> str:
    """Wait for a specific key or mouse button to be pressed.
    
    Waits for the specified key symbol to be pressed, or until the timeout period expires.
    
    :param key_sym: the key symbol to detect
    :type key_sym: str
    :param timeout: the maximum time to wait in milliseconds, or 0 for no timeout
    :type timeout: int
    :return: the key symbol that was pressed, or an empty string if timeout occurred
    :rtype: str
    """
    rounds = timeout / 100
    if timeout == 0:
        rounds = maxint()
    status = TurtleCanvas._pressed_keys.get(key_sym, 0)
    TurtleCanvas._pressed_keys[key_sym] = 0
    while not TurtleCanvas._pressed_keys.get(key_sym) and rounds > 0:
        rounds -= 1
        pause(100)
    # restore previous status if it timed out
    if rounds == 0:
        TurtleCanvas._pressed_keys[key_sym] = status
        return ""
    return get_key_sym()

def get_clickx() -> int:
    """Return the x-coordinate of the last mouse click.
    
    The coordinate is scaled according to the canvas resolution.
    
    :return: the x-coordinate of the last mouse click
    :rtype: int
    """
    return int(TurtleCanvas._pressed_keys["clickx"] / TurtleCanvas._x_multiplier + TurtleCanvas._origin_x)

def get_clicky() -> int:
    """Return the y-coordinate of the last mouse click.
    
    The coordinate is scaled according to the canvas resolution.
    
    :return: the y-coordinate of the last mouse click
    :rtype: int
    """
    return int(TurtleCanvas._pressed_keys["clicky"] / TurtleCanvas._y_multiplier + TurtleCanvas._origin_y)

def get_click() -> int:
    """Return the mouse button that was clicked.
    
    :return: the identifier of the mouse button that was clicked
    :rtype: int
    """
    return TurtleCanvas._pressed_keys["click"]


# Returns 0 for a key that was never pressed, kshift for one currently pressed and -kshift for one that was released
def status(key_sym: str):
    """Return the status of a key or mouse button.
    
    :param key_sym: the key symbol to check the status of
    :type key_sym: str
    :return: 0 for a key that was never pressed, kshift for one currently pressed and -kshift for one that was released
    :rtype: int
    """
    return TurtleCanvas._pressed_keys.get(key_sym, 0)


def reset(key_sym: str):
    """Reset the status of a key or mouse position.
    
    :param key_sym: the key symbol to reset
    :type key_sym: str
    """
    if key_sym == "mousex":
        TurtleCanvas._mousex = -1
    elif key_sym == "mousey":
        TurtleCanvas._mousey = -1
    else:
        TurtleCanvas._pressed_keys[key_sym] = 0


# turtle operations
def new_turtle(turtle: Turtle):
    """Adds a new turtle to the Canvas and switches to it.

    :param turtle: the new turtle to use
    :type turtle: Turtle
    """
    TurtleCanvas._turtles.append(turtle)
    TurtleCanvas._current_turtle_index = len(TurtleCanvas._turtles) - 1

    if turtle.layer not in TurtleCanvas._layers:
        TurtleCanvas._layers.append(turtle.layer)
        TurtleCanvas._layers.sort()

def change_turtle(idx: int):
    """Changes to a different turtle in the turtles array.

    :param idx: the index of the turtle to switch to
    :type idx: int
    """
    TurtleCanvas._current_turtle_index = idx

def remove_turtle(idx: int):
    """Removes a turtle from the turtles array.

    :param idx: the index of the turtle to remove
    :type idx: int
    """
    if 0 <= idx < len(TurtleCanvas._turtles):
        del TurtleCanvas._turtles[idx]
        # If current turtle was removed, switch to the last turtle
        TurtleCanvas._current_turtle_index = min(TurtleCanvas._current_turtle_index, len(TurtleCanvas._turtles) - 1)

def turtles() -> list[Turtle]:
    """Return a list of all turtles.

    :return: a list of all turtles
    :rtype: list[Turtle]
    """
    return TurtleCanvas._turtles

def current_turtle() -> Turtle:
    """Return the currently active turtle.

    :return: the currently active turtle
    :rtype: Turtle
    """
    return TurtleCanvas._turtles[TurtleCanvas._current_turtle_index]

# non-canvas operations
def randcol(n: int) -> int:
    """Return a random colour from the colour list.
    
    :param n: the number of colours to consider (selects from indices 0 to n-1)
    :type n: int
    :return: a random colour from the colour list
    :rtype: int
    """
    return colour_list[random.randint(0, n - 1)]


def rgb(n: int) -> int:
    """Return a colour from the colour list.
    
    :param n: the index of the colour to return
    :type n: int
    :return: the colour at the specified index in the colour list
    :rtype: int
    """
    return colour_list[n]


def mixcols(col1: int | str, col2: int | str, prop1: int, prop2: int) -> int:
    """Mix two colours in the given proportions.
    
    :param col1: the first colour to mix
    :type col1: int | str
    :param col2: the second colour to mix
    :type col2: int | str
    :param prop1: the proportion of the first colour
    :type prop1: int
    :param prop2: the proportion of the second colour
    :type prop2: int
    :return: the mixed colour
    :rtype: int
    """
    col1 = colour_to_int(col1)
    col2 = colour_to_int(col2)
    return (col1 * prop1 + col2 * prop2) // (prop1 + prop2)


def divmult(a: int, b: int, c: int) -> int:
    """Divide a by b, multiply by c, and round to the nearest integer.
    
    :param a: the numerator
    :type a: int
    :param b: the denominator
    :type b: int
    :param c: the multiplier
    :type c: int
    :return: the result of (a/b)*c, rounded to the nearest integer
    :rtype: int
    """
    return int(round(a / b * c))


def maxint() -> int:
    """Return the maximum integer value.

    :return: the maximum integer value
    :rtype: int
    """
    return sys.maxsize


def antilog(a: int, b: int, mult: int) -> int:
    """Calculate the antilogarithm (base 10) of a given value and multiply by a factor.
    :param a: the numerator of the quantity to find the antilogarithm of
    :type a: int
    :param b: the denominator of the quantity to find the antilogarithm of
    :type b: int
    :param mult: the multiplier to apply to the result
    :type mult: int
    :return: the antilogarithm of a/b multiplied by mult
    :rtype: int
    """
    return math.pow(10, a / b) * mult


def delete(s: str, idx: int, l: int) -> str:
    """Delete a substring from a string.

    :param s: the original string
    :type s: str
    :param idx: the starting index of the substring to delete
    :type idx: int
    :param l: the length of the substring to delete
    :type l: int
    :return: the modified string with the substring removed
    :rtype: str
    """
    return s[:idx] + s[idx + l:]


def pad(s: str, padding: string, length: int) -> str:
    """Pad a string with a specified character to a given length.

    :param s: the original string
    :type s: str
    :param padding: the character to pad with
    :type padding: str
    :param length: the desired length of the string
    :type length: int
    :return: the padded string
    :rtype: str
    """

    return s.ljust(length, padding)


def intdef(s, default: int) -> int:
    """Convert the given value to an integer, returning a default value if conversion fails.

    :param s: the value to convert
    :param default: the default value to return if conversion fails
    :type default: int
    :return: the converted integer value or the default value
    :rtype: int
    """

    try:
        return int(s)
    except ValueError:
        return default


def qstr(a: int, b: int, decplaces: int) -> str:
    """Format a division result as a string with a specified number of decimal places.

    :param a: the numerator
    :type a: int
    :param b: the denominator
    :type b: int
    :param decplaces: the number of decimal places to format to
    :type decplaces: int
    :return: the formatted string
    :rtype: str
    """

    s = "{:." + str(decplaces) + "f}"
    return s.format(a / b)


def qint(s: str, mult: int, default: int) -> int:
    """Convert a string to a float, multiplying by a factor, and rounding it, and returning a default value if conversion fails.

    :param s: the string to convert
    :type s: str
    :param mult: the multiplier to apply to the result
    :type mult: int
    :param default: the default value to return if conversion fails
    :type default: int
    :return: the converted integer value or the default value
    :rtype: int
    """

    try:
        return round(float(s) * mult)
    except ValueError:
        return default
    
def qval(s: str, mult: int, default: int) -> int:
    try:
        return round(float(s) * mult)
    except ValueError:
        return default

def halt(e: Event = None):
    TurtleCanvas._canvas.mainloop()
    exit(0)

def cos(x: float) -> float:
    """
    Return the cosine of x.

    :param x: the value (in angle units) to find the cosine of
    :type x: float

    :return: the cosine of x.
    :rtype float
    """
    return math.cos(math.radians(x / TurtleCanvas._angles * 360))

def acos(x: float) -> float:
    """
    Return the arc cosine of x in angle units.

    :param x: the value to find the arc cosine of.
    :type x: float

    :return: the arc cosine of x in angle units.
    :rtype float
    """
    return _degs_to_angle_units(math.degrees(math.acos(x)))

def sin(x: float) -> float:
    """
    Return the sine of x.

    :param x: the value (in angle units) to find the sine of
    :type x: float

    :return: the sine of x.
    :rtype float
    """
    return math.sin(math.radians(x / TurtleCanvas._angles * 360))

def asin(x: float) -> float:
    """
    Return the arc sine of x in angle units.

    :param x: the value to find the arc sine of.
    :type x: float

    :return: the arc sine of x in angle units.
    :rtype float
    """
    return _degs_to_angle_units(math.degrees(math.asin(x)))

def tan(x: float) -> float:
    """
    Return the tangent of x.

    :param x: the value (in angle units) to find the tangent of
    :type x: float

    :return: the tangent of x.
    :rtype float
    """
    return math.tan(math.radians(x / TurtleCanvas._angles * 360))

def atan(x: float) -> float:
    """
    Return the arc tangent of x in angle units.

    :param x: the value to find the arc tangent of.
    :type x: float

    :return: the arc tangent of x in angle units.
    :rtype float
    """
    return _degs_to_angle_units(math.degrees(math.atan(x)))

def chdir(path: str):
    """Changes the current working directory to the specified path.

    :param path: the new directory to change to.
    """
    os.chdir(path)

def checkfile(pcode: str, file_name: str) -> str:
    """
    Perform file operations on the current working directory using the given PCode.
    bits 0-1: code AND 3 determines one of four different overall actions: 
    0 merely enquires about the presence of a file with the specified name; 
    1 deletes the file if it is present; 
    2 creates it if not present; 
    3 likewise creates it if not present, but if it already exists, recreates it anew. 
    
    bits 2-3: code AND 12 determines the notification level if no file initially exists: 
    0 is silent; 
    4 merely informs of its non-existence; 
    8 warns of its non-existence; 
    12 stops the program with an error message. 
    
    bits 4-5: code AND 48 determines the notification level if the file initially exists: 
    0 is silent; 16 merely informs of its existence; 
    32 warns of its existence; 
    48 stops the program with an error message. 
    Whatever the code value may be, if an attempt to create or delete the file fails, then the programs stops with an error message. 

    bits 6-7: should be 0 on entry. 
    On exit, bit 6 is set if and only if the file existed prior to the instruction, while bit 7 is set if and only if the file existed after the instruction. 
    
    The lower bits of code remain unchanged on exit.

    :param pcode: A binary string PCode to use for the file operations.
    :type pcode: str
    :param file_name: the name of the file to perform the operations on.
    :type file_name: str
    
    :return: the PCode after the file operations.
    :rtype: str
    """

    # Check if PCode is valid
    if len(pcode) != 8:
        raise ValueError("PCode must be 8 characters long")
    if not all(bit in "01" for bit in pcode):
        raise ValueError("PCode must be a binary string")
    
    code = int(pcode, 2)
    action = code & 3
    non_exist_level = code & 12    # bits 2-3
    exist_level = code & 48        # bits 4-5

    existed_before = os.path.exists(file_name)

    if action == 0:  # Inquiry: do nothing
        pass
    elif action == 1:  # Delete file if exists
        if existed_before:
            try:
                os.remove(file_name)
            except Exception as e:
                raise RuntimeError("Deletion failed") from e
        else:
            if non_exist_level == 4:
                print(f"File {file_name} does not exist.")
            elif non_exist_level == 8:
                print(f"\033[33mWarning: File {file_name} does not exist.\033[0m")
            elif non_exist_level == 12:
                raise FileNotFoundError(f"\033[31mError: File {file_name} does not exist.\033[0m")
    elif action == 2:  # Create if not present
        if not existed_before:
            try:
                open(file_name, "w").close()
            except Exception as e:
                raise RuntimeError("Creation failed") from e
        else:
            if exist_level == 16:
                print(f"File {file_name} already exists.")
            elif exist_level == 32:
                print(f"\033[33mWarning: File {file_name} already exists.\033[0m")
            elif exist_level == 48:
                raise FileExistsError(f"\033[31mError: File {file_name} already exists.\033[0m")
    elif action == 3:  # Recreate: if exists, delete then create
        if existed_before:
            if exist_level == 16:
                print(f"File {file_name} exists and will be recreated.")
            elif exist_level == 32:
                print(f"\033[33mWarning: File {file_name} exists and will be recreated.\033[0m")
            elif exist_level == 48:
                raise FileExistsError(f"\033[31mError: File {file_name} exists.\033[0m")
            try:
                os.remove(file_name)
            except Exception as e:
                raise RuntimeError("Deletion failed during recreation") from e
        try:
            open(file_name, "w").close()
        except Exception as e:
            raise RuntimeError("Creation failed during recreation") from e

    existed_after = os.path.exists(file_name)
    bit6 = 1 if existed_before else 0
    bit7 = 1 if existed_after else 0
    new_code = code | (bit6 << 6) | (bit7 << 7)
    return format(new_code, '08b')

def checkdir(pcode: str, dir_name: str) -> str:
    """Perform directory operations on the current working directory using the given PCode.
    
    Similar to checkfile function but operates on directories instead of files.
    
    bits 0-1: code AND 3 determines one of four different overall actions: 
    0 merely enquires about the presence of a directory with the specified name; 
    1 deletes the directory if it is present; 
    2 creates it if not present; 
    3 likewise creates it if not present, but if it already exists, recreates it anew. 
    
    bits 2-3: code AND 12 determines the notification level if no directory initially exists: 
    0 is silent; 4 merely informs of its non-existence; 
    8 warns of its non-existence; 12 stops the program with an error message. 
    
    bits 4-5: code AND 48 determines the notification level if the directory initially exists: 
    0 is silent; 16 merely informs of its existence; 
    32 warns of its existence; 48 stops the program with an error message. 
    
    bits 6-7: should be 0 on entry. 
    On exit, bit 6 is set if and only if the directory existed prior to the instruction, 
    while bit 7 is set if and only if the directory existed after the instruction.
    
    :param pcode: A binary string PCode to use for the directory operations
    :type pcode: str
    :param dir_name: the name of the directory to perform the operations on
    :type dir_name: str
    
    :return: the PCode after the directory operations
    :rtype: str
    """
    # Validate PCode
    if len(pcode) != 8:
        raise ValueError("PCode must be 8 characters long")
    if not all(bit in "01" for bit in pcode):
        raise ValueError("PCode must be a binary string")
    
    code = int(pcode, 2)
    action = code & 3
    non_exist_level = code & 12    # bits 2-3
    exist_level = code & 48        # bits 4-5

    existed_before = os.path.isdir(dir_name)

    if action == 0:  # Inquiry: do nothing
        pass
    elif action == 1:  # Delete directory if exists
        if existed_before:
            try:
                shutil.rmtree(dir_name)
            except Exception as e:
                raise RuntimeError("\033[31mDeletion failed\033[0m") from e
        else:
            if non_exist_level == 4:
                print(f"Directory {dir_name} does not exist.")
            elif non_exist_level == 8:
                print(f"\033[33mWarning: Directory {dir_name} does not exist.\033[0m")
            elif non_exist_level == 12:
                raise FileNotFoundError(f"\033[31mError: Directory {dir_name} does not exist.\033[0m")
    elif action == 2:  # Create directory if not present
        if not existed_before:
            try:
                os.makedirs(dir_name)
            except Exception as e:
                raise RuntimeError("\033[31mCreation failed\033[0m") from e
        else:
            if exist_level == 16:
                print(f"Directory {dir_name} already exists.")
            elif exist_level == 32:
                print(f"\033[33mWarning: Directory {dir_name} already exists.\033[0m")
            elif exist_level == 48:
                raise FileExistsError(f"\033[31mError: Directory {dir_name} already exists.\033[0m")
    elif action == 3:  # Recreate: delete if exists then create
        if existed_before:
            if exist_level == 16:
                print(f"Directory {dir_name} exists and will be recreated.")
            elif exist_level == 32:
                print(f"\033[33mWarning: Directory {dir_name} exists and will be recreated.\033[0m")
            elif exist_level == 48:
                raise FileExistsError(f"\033[31mError: Directory {dir_name} exists.\033[0m")
            try:
                shutil.rmtree(dir_name)
            except Exception as e:
                raise RuntimeError("\033[31mDeletion failed during recreation\033[0m") from e
        try:
            os.makedirs(dir_name)
        except Exception as e:
            raise RuntimeError("\033[31mCreation failed during recreation\033[0m") from e

    existed_after = os.path.isdir(dir_name)
    bit6 = 1 if existed_before else 0
    bit7 = 1 if existed_after else 0
    new_code = code | (bit6 << 6) | (bit7 << 7)
    return format(new_code, '08b')

def console(clear: bool, colour: int):
    """Clear and/or recolour console

    :param clear: whether to clear the console
    :type clear: bool
    :param colour: the colour to set the console to
    :type colour: int
    """

    if clear:
        os.system("cls" if os.name == "nt" else "clear") # Clear the console (cls for Windows, clear for Unix)
    if colour != -1:
        os.system(f"color {colour.to_bytes(3, 'big').hex()}") # Recolour console

def eof(file_handle) -> bool:
    """Check if the file handle is at the end of the file.

    :param file_handle: the file handle to check
    :type file_handle: file
    :return: True if the file handle is at the end of the file, False otherwise
    :rtype: bool
    """

    curr = file_handle.tell()
    ch = file_handle.read(1)
    file_handle.seek(curr)
    return ch == ""

def eoln(file_handle) -> bool:
    """Check if the file handle is at the end of a line.
    
    :param file_handle: the file handle to check
    :type file_handle: file
    :return: True if the file handle is at the end of a line, False otherwise
    :rtype: bool
    """

    curr = file_handle.tell()
    ch = file_handle.read(1)
    file_handle.seek(curr)
    return ch == "\n"

def exp(x: float) -> float:
    """Return e raised to the power of x.

    :param x: the exponent to raise e to
    :type x: float
    :return: e raised to the power of x
    :rtype: float
    """

    return math.exp(x)

def log(x: float) -> float:
    """Return the natural logarithm of x.

    :param x: the value to find the natural logarithm of
    :type x: float
    :return: the natural logarithm of x
    :rtype: float
    """

    return math.log(x)

def log10(x: float) -> float:
    """Return the base-10 logarithm of x.

    :param x: the value to find the base-10 logarithm of
    :type x: float
    :return: the base-10 logarithm of x
    :rtype: float
    """

    return math.log10(x)

def power(base: float, power: float) -> float:
    """Return the value of base raised to the power.

    :param base: the base value
    :type base: float
    :param power: the power to raise the base to
    :type power: float
    :return: base raised to the power
    :rtype: float
    """

    return math.pow(base, power)

def sqrt(x: float) -> float:
    """Return the square root of x.

    :param x: the value to find the square root of
    :type x: float
    :return: the square root of x
    :rtype: float
    """

    return math.sqrt(x)

def pi() -> float:
    return math.pi

file: TypeAlias = IO
def fopen(path: str, mode: int) -> file:
    """Open a file with the specified mode.
    Mode 1 = read
    Mode 2 = append
    Mode 3 = write

    :param path: the path to the file
    :type path: str
    :param mode: the mode to open the file in
    :type mode: int
    :return: the file object
    :rtype: file
    """

    if mode == 1:
        return open(path, "r")
    elif mode == 2:
        return open(path, "a")
    elif mode == 3:
        return open(path, "w")
    else:
        raise ValueError("Invalid mode")

def fclose(file_to_close: file):
    """ Close the file

    :param file_handle: the file object to close
    :type file_handle: file
    """
    file_to_close.close()


def fmove(file_to_move: file, new_path: str) -> bool:
    """Move the file object to the new path

    :param file_to_move: the file object to move
    :type file_to_move: file
    :param new_path: the new path to the file
    :type new_path: str
    :return: True if the move operation was successful. False if it was not.
    :rtype: bool
    """
    try:
        file_name = file_to_move.name
        file_to_move.close()
        shutil.move(file_name, new_path)
        return True
    except Exception as e:
        print(f"Error moving file: {e}")
        return False


def fcopy(file_to_copy: file) -> file:
    """Copy the file to a new file object

    :param file_to_copy: the file object to copy
    :type file_to_copy: file
    :return: a new file object that is a copy of the original
    :rtype: file
    """
    try:
        file_name = file_to_copy.name
        mode = file_to_copy.mode if hasattr(file_to_copy, 'mode') else 'r'
        file_to_copy.flush()
        copy_name = file_name + ".copy"
        shutil.copy(file_name, copy_name)
        return open(copy_name, mode)
    except Exception as e:
        print(f"Error copying file: {e}")


def fread(file_to_read: file):
    """Read the file and return its contents

    :param file_to_read: the file object to read
    :type file_to_read: file
    :return: the contents of the file
    """
    return file_to_read.read()


def freadline(file_to_read: file):
    """Read a line from the file and return its contents

    :param file_to_read: the file object to read
    :type file_to_read: file
    :return: a line from the file
    """
    return file_to_read.readline()

def fremove(file_to_remove: file):
    """Delete the file

    :param file_to_remove: the file object to delete
    :type file_to_remove: file
    """
    file_name = file_to_remove.name
    file_to_remove.close()
    os.remove(file_name)

def frestart(file_to_restart: file):
    """Restart the file

    :param file_to_restart: the file object to restart
    :type file_to_restart: file
    """
    file_to_restart.seek(0)

def fwrite(file_to_write: file, data: str):
    """Write data to the file

    :param file_to_write: the file object to write to
    :type file_to_write: file
    :param data: the data to write to the file
    :type data: str
    """
    file_to_write.write(data)

def fwriteline(file_to_write: file, data: str):
    """Write a line to the file

    :param file_to_write: the file object to write to
    :type file_to_write: file
    :param data: the data to write to the file
    :type data: str
    """
    file_to_write.write(data + "\n")

def _find_dirs_files(pattern: str) -> list[str]:
    """Helper function. Finds all instances that match the pattern in the directory

    :param pattern: the pattern to match
    :type pattern: str
    :return: a list of all instances that match the pattern in the directory
    :rtype: list[str]
    """
    pattern = os.path.join(os.getcwd(), pattern)
    return glob.glob(pattern, root_dir=os.getcwd)

"""A type alias for a mutable handle to store the index of the found directory or file.
This is a workaround for the fact that Python does not support mutable integers.
"""
FindHandle: TypeAlias = list[int]

def finddir(pattern: str, find_handle: FindHandle) -> str:
    """Find the first directory that matches the pattern.
    Modifies the find_handle tuple to store the index of the handle that was found.
    
    :param pattern: the pattern to match
    :type pattern: str
    :param find_handle: the handle to store the index of the directory that was found.
    :type find_handle: FindHandle
    :return: the name of the directory that matches the pattern
    :rtype: str
    """
    # Fix empty find handle
    if len(find_handle) == 0:
        find_handle.append(0)

    TurtleCanvas._dir_search_results = list(filter(os.path.isdir, _find_dirs_files(pattern))) # Store all directories that match the pattern
    return TurtleCanvas._dir_search_results[0]

def findfirst(pattern: str,  find_handle: FindHandle) -> str:
    """Find the first file that matches the pattern.
    
    :param pattern: the pattern to match
    :type pattern: str
    :param find_handle: the handle to store the index of the file that was found
    :type find_handle: FindHandle
    :return: the name of the first file that matches the pattern
    :rtype: str
    """
    # Fix empty find handle
    if len(find_handle) == 0:
        find_handle.append(0)

    TurtleCanvas._file_search_results = list(filter(os.path.isfile, _find_dirs_files(pattern))) # Store all files that match the pattern
    find_handle[0] = 1 # Sets index to the second element (for subsequent findnext commands)
    return TurtleCanvas._file_search_results[0]

def findnext(find_handle: list[int]) -> str:
    """Find the next file that matches the pattern.
    
    :param find_handle: the handle to store the index of the file that was found
    :type find_handle: FindHandle
    :return: the name of the next file that matches the pattern
    :rtype: str
    """

    # Fix empty find handle
    if len(find_handle) == 0:
        find_handle.append(0)

    file = TurtleCanvas._file_search_results[find_handle[0]] # Use the files stored in the search results
    find_handle[0] += 1 # Increment index
    return file

def hypot(a: float, b: float) -> float:
    """Return the hypotenuse of a right-angled triangle with sides a and b.

    :param a: the length of the first side
    :type a: float
    :param b: the length of the second side
    :type b: float
    :return: the length of the hypotenuse
    :rtype: float
    """
    return math.hypot(a, b)

def isdir(path: str) -> bool:
    """Check if the path is a directory.

    :param path: the path to check
    :type path: str
    :return: True if the path is a directory, False otherwise
    :rtype: bool
    """
    return os.path.isdir(path)

def isfile(path: str) -> bool:
    """Check if the path is a file.

    :param path: the path to check
    :type path: str
    :return: True if the path is a file, False otherwise
    :rtype: bool
    """
    return os.path.isfile(path)

def sign(x: float) -> int:
    """Return the sign of x.

    :param x: the value to find the sign of
    :type x: float
    :return: 1 if x is positive, -1 if x is negative, 0 if x is 0
    :rtype: int
    """
    return 1 if x > 0 else -1 if x < 0 else 0

def keybuffer(size: int):
    """Create a key buffer of the specified size.

    :param size: the size of the key buffer
    :type size: int
    """
    TurtleCanvas._key_buffer_size = size
    TurtleCanvas._key_buffer = []

def keyecho(on: bool):
    """Turn on or off key echo to console

    :param on: True to turn on key echo, False to turn it off
    :type on: bool
    """
    TurtleCanvas._key_echo = on

def read(max_size: int) -> str:
    """Read a string from the keyboard buffer of the specified size.

    :param max_size: the maximum size of the string to read
    :type max_size: int
    :return: the string read from the keyboard buffer
    :rtype: str
    """
    if len(TurtleCanvas._key_buffer) == 0:
        return ""
    return TurtleCanvas._key_buffer[:min(max_size, len(TurtleCanvas._key_buffer))] # Return the first max_size characters

def mkdir(name: str) -> bool:
    """Create a new directory with the specified name.

    :param name: the name of the new directory
    :type name: str
    :return: True if the directory was created successfully, False otherwise
    :rtype: bool
    """
    try:
        os.mkdir(name)
        return True
    except Exception as e:
        print(f"Error creating directory: {e}")
        return False
    
def rmdir(name: str) -> bool:
    """Remove the directory with the specified name.

    :param name: the name of the directory to remove
    :type name: str
    :return: True if the directory was removed successfully, False otherwise
    :rtype: bool
    """
    try:
        os.rmdir(name)
        return True
    except Exception as e:
        print(f"Error removing directory: {e}")
        return False

def mkfile(name: str) -> bool:
    """Create a new file with the specified name.

    :param name: the name of the new file
    :type name: str
    :return: True if the file was created successfully, False otherwise
    :rtype: bool
    """
    try:
        open(name, "w").close()
        return True
    except Exception as e:
        print(f"Error creating file: {e}")
        return False
    
def root(radicand: float, index: float) -> float:
    """Return the index-th root of the radicand.

    :param radicand: the value to find the root of
    :type radicand: float
    :param index: the index of the root
    :type index: float
    :return: the index-th root of the radicand
    :rtype: float
    """
    return radicand ** (1 / index)

def recolour(x1: int, y1: int, x2: int, y2: int, colour: int):
    """Recolour the specified area of the canvas.

    :param x1: the x-coordinate of the top-left corner of the area
    :type x1: int
    :param y1: the y-coordinate of the top-left corner of the area
    :type y1: int
    :param x2: the x-coordinate of the bottom-right corner of the area
    :type x2: int
    :param y2: the y-coordinate of the bottom-right corner of the area
    :type y2: int
    :param colour: the colour to set the area to
    :type colour: int
    """
    return TurtleCanvas._canvas.create_rectangle(
        _scale_x(x1),
        _scale_y(y1),
        _scale_x(x2),
        _scale_y(y2),
        fill=colour_to_str(colour),
        width=0,
        tags=f"layer{TurtleCanvas._layer}",
    )

def randint(a: int, b: int) -> int:
    """Return a random integer between a and b (inclusive).

    :param a: the lower bound of the random integer
    :type a: int
    :param b: the upper bound of the random integer
    :type b: int
    :return: a random integer between a and b
    :rtype: int
    """
    return random.randint(a, b)

def randrange(range: int) -> int:
    """Return a random integer between 0 and range - 1 (exclusive).

    :param range: the upper bound of the random integer
    :type range: int
    :return: a random integer between 0 and range
    :rtype: int
    """
    return random.randrange(range)

def randseed(seed: int):
    """Set the seed for the random number generator.

    :param seed: the seed to set
    :type seed: int
    """
    random.seed(seed)

def time() -> int:
    """Return the time in milliseconds since the start of the programme.

    :return: the time in milliseconds
    :rtype: int
    """
    return int((datetime.now() - TurtleCanvas._time).total_seconds() * 1000)

def timeset(millis: int):
    """Set the time to the specified value.

    :param millis: the time to set
    :type millis: int
    """
    TurtleCanvas._time = millis

__module__ = "turtle_oxford_plus"