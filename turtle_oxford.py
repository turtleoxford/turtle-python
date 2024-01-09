from contextlib import contextmanager
import logging
import math
from PIL import ImageColor
from time import sleep
from tkinter import *


class TurtleCanvas:
    # Turtle vars
    _direction: int = 0
    _angles: int = 360
    _x: int = 0
    _y: int = 0
    _thick: int = 1
    _colour: str = "white"
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
    # Possible values: 1, -1 (pressed and released respectively)
    _pressed_keys: dict[str, int] = {}

    def create(
        self,
        origin_x: int = 0,
        origin_y: int = 0,
        width: int = 500,
        height: int = 500,
    ):
        TurtleCanvas._width = width
        TurtleCanvas._height = height
        TurtleCanvas._root = Tk()
        TurtleCanvas._root.title("Turtle")

        self._frame = Frame(self._root, width=TurtleCanvas._width, height=TurtleCanvas._height+100)
        self._frame.pack(expand=True, fill=BOTH)
        self._halt = Button(self._frame, text="HALT")
        self._halt.pack()

        TurtleCanvas._canvas = Canvas(
            self._frame, bg="white", width=width, height=height
        )
        TurtleCanvas._canvas.pack(side="bottom")
        TurtleCanvas._canvas.focus_set()
        TurtleCanvas._canvas.bind("<KeyPress>", on_key_press)
        TurtleCanvas._canvas.bind("<KeyRelease>", on_key_release)

        self._halt.bind("<ButtonPress>", lambda e: TurtleCanvas._canvas.mainloop())

        TurtleCanvas._origin_x, TurtleCanvas._origin_y = origin_x, origin_y
        TurtleCanvas._home = width / 2, height / 2
        TurtleCanvas._x, TurtleCanvas._y = TurtleCanvas._home


    def refresh():
        if not TurtleCanvas._canvas:
            logging.error("Canvas not lanuched, please create a canvas first.")
        TurtleCanvas._root.update()


@contextmanager
def turtle_canvas(
    origin_x: int = 0, origin_y: int = 0, width: int = 500, height: int = 500
):
    canvas = TurtleCanvas()
    try:
        canvas.create(origin_x, origin_y, width, height)
        yield canvas
    except TclError:
        logging.debug("Window closed")
    finally:
        TurtleCanvas._canvas.mainloop()


# Change canvas
def update():
    TurtleCanvas._update = True
    TurtleCanvas.refresh()


def noupdate():
    TurtleCanvas._update = False


def resolution(x: int, y: int):
    TurtleCanvas._x_multiplier = TurtleCanvas._width / x
    TurtleCanvas._y_multiplier = TurtleCanvas._height / y
    TurtleCanvas._canvas.scale(
        "all",
        0, 
        0,
        TurtleCanvas._x_multiplier,
        TurtleCanvas._y_multiplier,
    )


# Change coordinates
def home():
    setxy(TurtleCanvas._home)


def setx(x: int):
    TurtleCanvas._x = x


def sety(y: int):
    TurtleCanvas._y = y


def setxy(x: int, y: int):
    TurtleCanvas._x = x
    TurtleCanvas._y = y


# Change colour


def colour_to_int(colour: tuple[int, int, int] | int | str) -> int:
    if isinstance(colour, int):
        return colour
    elif isinstance(colour, str):
        return colour_to_int(ImageColor.getrgb(colour))
    elif isinstance(colour, tuple):
        r, g, b = colour
        return (r << 16) + (g << 8) + b


def colour_to_str(colour: tuple[int, int, int] | int | str) -> str:
    if isinstance(colour, str):
        return colour
    elif isinstance(colour, tuple):
        r, g, b = colour
        # hex strings start with 0x so we strip that to create the colour hex
        return f"#{hex(r)[2:]}{hex(g)[2:]}{hex(b)[2:]}"
    elif isinstance(colour, int):
        return f"#{colour.to_bytes(3, 'big').hex()}"


def colour(new_colour: tuple[int, int, int] | int | str):
    TurtleCanvas._colour = colour_to_str(new_colour)


# Change pen


def thickness(new_thickness: int):
    TurtleCanvas._thick = new_thickness


def penup():
    TurtleCanvas._pen = False


def pendown():
    TurtleCanvas._pen = True


def pause(duration: int):
    sleep(duration / 1000)
    TurtleCanvas.refresh()


# Change direction


def right(degrees: int):
    TurtleCanvas._direction = (TurtleCanvas._direction - degrees) % 360


def left(degrees: int):
    TurtleCanvas._direction = (TurtleCanvas._direction + degrees) % 360


def direction(degrees: int):
    TurtleCanvas._direction = degrees


# Draw shapes

# Define a decorator for the drawing functions which handles the drawing boilerplate
def draw(func: callable) -> callable:
    def inner(*args, **kwargs) -> int:
        id: int = func(*args, **kwargs)
        if TurtleCanvas._update:
            TurtleCanvas.refresh()
        TurtleCanvas._canvas.focus_set()
        return id

    return inner


@draw
def forward(distance: int) -> int:
    new_y = TurtleCanvas._y - distance * math.cos(math.radians(TurtleCanvas._direction))
    new_x = TurtleCanvas._x - distance * math.sin(math.radians(TurtleCanvas._direction))
    id = TurtleCanvas._canvas.create_line(
        (TurtleCanvas._x - TurtleCanvas._origin_x) * TurtleCanvas._x_multiplier,
        (TurtleCanvas._y - TurtleCanvas._origin_y) * TurtleCanvas._y_multiplier,
        (new_x - TurtleCanvas._origin_x) * TurtleCanvas._x_multiplier,
        (new_y - TurtleCanvas._origin_y) * TurtleCanvas._x_multiplier,
        fill=TurtleCanvas._colour,
        width=TurtleCanvas._thick * TurtleCanvas._x_multiplier,
    )
    TurtleCanvas._x = new_x
    TurtleCanvas._y = new_y
    return id


def blot(size: int):
    _disk(size, fill=True)


def circle(size):
    _disk(size, border=True)


@draw
def _disk(radius: int, border: bool = False, fill: bool = False) -> int:
    x1 = (TurtleCanvas._x - radius - TurtleCanvas._origin_x) * TurtleCanvas._x_multiplier
    y1 = (TurtleCanvas._y - radius - TurtleCanvas._origin_y) * TurtleCanvas._y_multiplier
    x2 = (TurtleCanvas._x + radius - TurtleCanvas._origin_x) * TurtleCanvas._x_multiplier
    y2 = (TurtleCanvas._y + radius - TurtleCanvas._origin_y) * TurtleCanvas._y_multiplier
    d = None
    if border:
        d = TurtleCanvas._canvas.create_oval(
            x1, y1, x2, y2, width=TurtleCanvas._thick * TurtleCanvas._x_multiplier, outline=TurtleCanvas._colour
        )
    if fill:
        d = TurtleCanvas._canvas.create_oval(
            x1, y1, x2, y2, width=0, fill=TurtleCanvas._colour
        )
    return d


@draw
def pixset(x: int, y: int, colour: int) -> int:
    pix = TurtleCanvas._canvas.create_rectangle(
        (x - TurtleCanvas._origin_x) * TurtleCanvas._x_multiplier,
        (y - TurtleCanvas._origin_y) * TurtleCanvas._y_multiplier,
        (x - TurtleCanvas._origin_x + 1) * TurtleCanvas._x_multiplier,
        (y - TurtleCanvas._origin_y + 1) * TurtleCanvas._y_multiplier,
        fill=colour_to_str(colour),
        width=0
    )
    return pix

@draw
def display(text: str, font: str="Helvetica", size: int=12) -> int:
    t = TurtleCanvas._canvas.create_text(
        TurtleCanvas._x,
        TurtleCanvas._y,
        anchor="nw",
        font=(f"{font} {size}"),
        fill=TurtleCanvas._colour,
        text=text)
    return t

@draw
def blank(colour) -> int:
    r = TurtleCanvas._canvas.create_rectangle(
        0, 0, 
        TurtleCanvas._width, TurtleCanvas._height, 
        fill=colour_to_str(colour), width=0
    )
    return r

# get information about the canvas
def pixcol(x: int, y: int) -> int:
    ids = TurtleCanvas._canvas.find_overlapping(
        (x - TurtleCanvas._origin_x) * TurtleCanvas._x_multiplier,
        (y - TurtleCanvas._origin_y) * TurtleCanvas._y_multiplier,
        (x - TurtleCanvas._origin_x + 1) * TurtleCanvas._x_multiplier,
        (y - TurtleCanvas._origin_y + 1) * TurtleCanvas._y_multiplier)
    if len(ids) == 0:
        # if no objects overlap, the pixel is white
        return colour_to_int("white")
    for id in reversed(ids):
        colour = TurtleCanvas._canvas.itemcget(id, "fill")
        if colour:
            return colour_to_int(colour)
    # All items overlapping the pixel are transparent
    return colour_to_int("white")

def get_key_sym() -> str:
    return TurtleCanvas._key_sym

def get_key_code() -> int:
    return TurtleCanvas._key_code

# user interactions

def on_key_press(event: Event):
    TurtleCanvas._key_code = event.keycode
    # This preserves the case for letters and removes the _L and _R from modifiers keys
    TurtleCanvas._key_sym = event.keysym.split("_")[0]
    TurtleCanvas._pressed_keys[TurtleCanvas._key_sym] = 1
    TurtleCanvas._pressed_keys["key"] = 1

    if event.keysym.startswith("Shift"):
        TurtleCanvas._kshift += 8
    elif event.keysym.startswith("Alt"):
        TurtleCanvas._kshift += 16
    elif event.keysym.startswith("Control"):
        TurtleCanvas._kshift += 32

def on_key_release(event: Event):
    TurtleCanvas._key_code = - event.keycode
    TurtleCanvas._pressed_keys[event.keysym] = -1

def detect(key_sym, timeout):
    rounds = timeout / 100
    if timeout == 0:
        rounds = 1 << 31
    status = TurtleCanvas._pressed_keys.get(key_sym, 0)
    TurtleCanvas._pressed_keys[key_sym] = 0
    while not TurtleCanvas._pressed_keys.get(key_sym) and rounds >= 0:
        rounds -=1
        pause(100)
    # restore previous status if it timed out
    if not TurtleCanvas._pressed_keys.get(key_sym) and status:
        TurtleCanvas._pressed_keys[key_sym] = status

# Returns 0 for a key that was never pressed, 1 for one currently pressed and -1 for one that was released
def get_key_status(key_sym):
    return TurtleCanvas._pressed_keys.get(key_sym, 0)

def reset(key_sym: str):
    if key_sym == "mouse":
        TurtleCanvas._mousex = -1
        TurtleCanvas._mousey = -1
    else:
        TurtleCanvas._pressed_keys[key_sym] = 0
