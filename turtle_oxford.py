"""
Turtle Oxford - a python library for the Oxford Turtle System
"""

from contextlib import contextmanager
import logging
import math
from PIL import ImageColor
from time import sleep
from tkinter import *
from constants import *
import random
import string
import sys


class TurtleCanvas:
    """Class with mostly static member describing the turtle and the canvas.
    """
    # Turtle vars
    _direction: int = 0
    _angles: int = 360
    _x: int = 0
    _y: int = 0
    _thick: int = 1
    _colour: str = "white"
    _history: list[tuple[int, int]] = []
    _old_turtle = []
    # Canvas vars
    _root: Tk | None = None
    _canvas: Canvas | None = None
    _home: tuple[int, int] = 0, 0
    _origin_x: int = 0
    _origin_y: int = 0
    _pen: bool = True
    _update: bool = True
    _x_multiplier: float = 1
    _y_multiplier: float = 1
    _width: int = 0
    _height: int = 0
    # Input vars
    _key_code: int = 0
    _key_sym: str = ""
    _kshift: int = 128
    # Possible values: +kshift, -kshift (pressed and released respectively)
    _pressed_keys: dict[str, int] = {}

    def create(
        self,
        origin_x: int = 0,
        origin_y: int = 0,
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
        TurtleCanvas._width = width
        TurtleCanvas._height = height
        TurtleCanvas._root = Tk()
        TurtleCanvas._root.title("Turtle")

        self._frame = Frame(
            self._root, width=TurtleCanvas._width, height=TurtleCanvas._height + 100
        )
        self._frame.pack(expand=True, fill=BOTH)
        self._halt = Button(self._frame, text="HALT")
        self._halt.pack()

        TurtleCanvas._canvas = Canvas(
            self._frame, bg="white", width=width, height=height
        )
        TurtleCanvas._canvas.pack(side="bottom")
        TurtleCanvas._canvas.focus_set()
        TurtleCanvas._canvas.bind("<KeyPress>", on_press)
        TurtleCanvas._canvas.bind("<KeyRelease>", on_release)
        TurtleCanvas._canvas.bind("<ButtonPress>", on_press)
        TurtleCanvas._canvas.bind("<ButtonRelease>", on_release)

        self._halt.bind("<ButtonRelease>", halt)

        TurtleCanvas._origin_x, TurtleCanvas._origin_y = origin_x, origin_y
        TurtleCanvas._home = width / 2, height / 2
        TurtleCanvas._x, TurtleCanvas._y = TurtleCanvas._home
        # TurtleCanvas._history.append(TurtleCanvas._home)

    def refresh():
        """
        Refresh the canvas to display the latest drawings.
        """
        if not TurtleCanvas._canvas:
            logging.error("Canvas not lanuched, please create a canvas first.")
        TurtleCanvas._root.update()


@contextmanager
def turtle_canvas(
    origin_x: int = 0, origin_y: int = 0, width: int = 500, height: int = 500
):
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
    canvas = TurtleCanvas()
    try:
        canvas.create(origin_x, origin_y, width, height)
        yield canvas
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


def resolution(x: int, y: int):
    """ Set the resolution of the canvas to x by y

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
    TurtleCanvas._direction = (
        TurtleCanvas._direction - degrees * 360 / TurtleCanvas._angles
    ) % 360


def left(degrees: int):
    """Turn left.

    :param degrees: number of degrees to turn left
    :type degrees: int
    """
    TurtleCanvas._direction = (
        TurtleCanvas._direction + degrees * 360 / TurtleCanvas._angles
    ) % 360


def direction(degrees: int):
    """Turtle changes direction to face this number of degrees.

    :param degrees: number of degrees that indicate a direction to face
    :type degrees: int
    """
    TurtleCanvas._direction = 360 / TurtleCanvas._angles * degrees


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
        (x - TurtleCanvas._origin_x) * TurtleCanvas._x_multiplier,
        (y - TurtleCanvas._origin_y) * TurtleCanvas._y_multiplier,
        (new_x - TurtleCanvas._origin_x) * TurtleCanvas._x_multiplier,
        (new_y - TurtleCanvas._origin_y) * TurtleCanvas._x_multiplier,
        fill=TurtleCanvas._colour,
        width=TurtleCanvas._thick * TurtleCanvas._x_multiplier,
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
    x1 = (
        TurtleCanvas._x - xradius - TurtleCanvas._origin_x
    ) * TurtleCanvas._x_multiplier
    y1 = (
        TurtleCanvas._y - yradius - TurtleCanvas._origin_y
    ) * TurtleCanvas._y_multiplier
    x2 = (
        TurtleCanvas._x + xradius - TurtleCanvas._origin_x
    ) * TurtleCanvas._x_multiplier
    y2 = (
        TurtleCanvas._y + yradius - TurtleCanvas._origin_y
    ) * TurtleCanvas._y_multiplier
    id = -1
    if border:
        id = TurtleCanvas._canvas.create_oval(
            x1,
            y1,
            x2,
            y2,
            width=TurtleCanvas._thick * TurtleCanvas._x_multiplier,
            outline=TurtleCanvas._colour,
        )
    if fill:
        id = TurtleCanvas._canvas.create_oval(
            x1, y1, x2, y2, width=0, fill=TurtleCanvas._colour
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
        (x - TurtleCanvas._origin_x) * TurtleCanvas._x_multiplier,
        (y - TurtleCanvas._origin_y) * TurtleCanvas._y_multiplier,
        (x - TurtleCanvas._origin_x + 1) * TurtleCanvas._x_multiplier,
        (y - TurtleCanvas._origin_y + 1) * TurtleCanvas._y_multiplier,
        fill=colour_to_str(colour),
        width=0,
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
        (TurtleCanvas._x - TurtleCanvas._origin_x) * TurtleCanvas._x_multiplier,
        (TurtleCanvas._y - TurtleCanvas._origin_y) * TurtleCanvas._y_multiplier,
        (TurtleCanvas._x - TurtleCanvas._origin_x + x) * TurtleCanvas._x_multiplier,
        (TurtleCanvas._y - TurtleCanvas._origin_y + y) * TurtleCanvas._y_multiplier,
        fill=colour_to_str(colour),
        width=int(border) * TurtleCanvas._thick,
    )


@draw
def polyline(n: int):
    """Draw a sequence of lines connecting the last n points the turtle has visited.

    :param n: the number of points to consider
    :type n: int
    """
    x, y = TurtleCanvas._x, TurtleCanvas._y
    for (old_x, old_y) in TurtleCanvas._history[-n:]:
        _draw_line(x, y, old_x, old_y)
        x, y = old_x, old_y


@draw
def polygon(n: int):
    """Draw a polygon using the last n points the turtle has visited.

    :param n: the number of points in the polygon
    :type n: int
    """
    TurtleCanvas._canvas.create_polygon(
        *TurtleCanvas._history[-n:], fill=colour_to_str(TurtleCanvas._colour)
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
    t = TurtleCanvas._canvas.create_text(
        TurtleCanvas._x,
        TurtleCanvas._y,
        anchor="nw",
        font=(f"{font} {size}"),
        fill=TurtleCanvas._colour,
        text=text,
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
    )
    return r


@draw
# If boundry is a negative number, then any colour is acceptable
def fill(x: int, y: int, boundry: int | str):
    if boundry.isinstance(str):
        boundry = colour_to_int(boundry)
    initcol = pixcol(x, y)

# get information about the canvas
def pixcol(x: int, y: int) -> int:
    ids = TurtleCanvas._canvas.find_overlapping(
        (x - TurtleCanvas._origin_x) * TurtleCanvas._x_multiplier,
        (y - TurtleCanvas._origin_y) * TurtleCanvas._y_multiplier,
        (x - TurtleCanvas._origin_x + 1) * TurtleCanvas._x_multiplier,
        (y - TurtleCanvas._origin_y + 1) * TurtleCanvas._y_multiplier,
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
    TurtleCanvas._kshift = 128

def on_press(event: Event):
    TurtleCanvas._kshift = 128

def on_press(event: Event):
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
        TurtleCanvas._pressed_keys["clickx"] = event.x
        TurtleCanvas._pressed_keys["clicky"] = event.y
        TurtleCanvas._pressed_keys["click"] = TurtleCanvas._key_code

    TurtleCanvas._pressed_keys[TurtleCanvas._key_sym] = TurtleCanvas._kshift
    TurtleCanvas._pressed_keys["mousekey"] = TurtleCanvas._kshift


def on_release(event: Event):
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
        TurtleCanvas._pressed_keys["clickx"] *= -1
        TurtleCanvas._pressed_keys["clicky"] *= -1
        TurtleCanvas._pressed_keys["click"] *= -1
    TurtleCanvas._pressed_keys["mousekey"] *= -1

def detect(key_sym, timeout) -> str:
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


# Returns 0 for a key that was never pressed, kshift for one currently pressed and -kshift for one that was released
def status(key_sym: str):
    return TurtleCanvas._pressed_keys.get(key_sym, 0)


def reset(key_sym: str):
    if key_sym == "mousex":
        TurtleCanvas._mousex = -1
    elif key_sym == "mousey":
        TurtleCanvas._mousey = -1
    else:
        TurtleCanvas._pressed_keys[key_sym] = 0


# turtle operations
def new_turtle(arr: list[int]):
    TurtleCanvas._old_turtle = [
        TurtleCanvas._x,
        TurtleCanvas._y,
        TurtleCanvas._direction,
        TurtleCanvas._thick,
        TurtleCanvas._colour,
    ]
    TurtleCanvas._x = arr[0]
    TurtleCanvas._y = arr[1]
    TurtleCanvas._direction = arr[2]
    TurtleCanvas._thick = arr[3]
    TurtleCanvas._colour = arr[4]


def old_turtle():
    TurtleCanvas._x = TurtleCanvas._old_turtle[0]
    TurtleCanvas._y = TurtleCanvas._old_turtle[1]
    TurtleCanvas._direction = TurtleCanvas._old_turtle[2]
    TurtleCanvas._thick = TurtleCanvas._old_turtle[3]
    TurtleCanvas._colour = TurtleCanvas._old_turtle[4]


# non-canvas operations
def randcol(n: int) -> int:
    return colour_list[random.randint(0, n - 1)]


def rgb(n: int) -> int:
    return colour_list[n]


def mixcols(col1: int | str, col2: int | str, prop1: int, prop2: int) -> int:
    col1 = colour_to_int(col1)
    col2 = colour_to_int(col2)
    return (col1 * prop1 + col2 * prop2) // (prop1 + prop2)


def divmult(a: int, b: int, c: int) -> int:
    return int(math.round(a / b * c))


def maxint() -> int:
    return sys.maxsize


def antilog(a: int, b: int, mult: int) -> int:
    return math.pow(10, a / b) * mult


def delete(s: str, idx: int, l: int) -> str:
    return s[:idx] + s[idx + len :]


def pad(s: str, padding: string, length: int) -> str:
    return s.ljust(length, padding)


def intdef(s, default: int) -> int:
    try:
        return int(s)
    except ValueError:
        return default


def qstr(a: int, b: int, decplaces: int) -> str:
    s = "{:." + str(decplaces) + "f}"
    return s.format(a / b)


def qint(s: str, mult: int, default: int) -> int:
    try:
        return round(float(s) * mult)
    except ValueError:
        return default


def halt(e: Event = None):
    TurtleCanvas._canvas.mainloop()
    exit(0)


__module__ = "turtle_oxford"
