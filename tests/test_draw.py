import time
import math
import sys
import pytest
import tkinter
from PIL import ImageColor
import os
from turtle_oxford import (TurtleCanvas, turtle_canvas) # Standard imports
from turtle_oxford import (_degs_to_angle_units, _scale_x, _scale_y) # Useful helpers
from turtle_oxford import (blot, circle, ellipse, ellblot, pixset, box, polyline, polygon, display, blank, recolour, fill, pixcol) # Functions under testing
TclError = tkinter.TclError  # in case needed

# Use a lambda to check if two floats are close (avoiding floating point errors)
is_close = lambda a, b: abs(a - b) < 1e-6

# Fixture to create a canvas and override mainloop so tests don't block
@pytest.fixture
def tc_setup():
    with turtle_canvas() as tc:
        # Monkey-patch mainloop to a no-op
        if TurtleCanvas._canvas:
            TurtleCanvas._canvas.mainloop = lambda: None
        # Reset state for tests
        TurtleCanvas._history = []
        yield tc

def test_blot(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Draw a blot with radius r
    r = 10
    blot_id = blot(r)

    # Check that the blot was drawn
    assert blot_id in TurtleCanvas._canvas.find_all()

    # Check that the blot was drawn at the correct coordinates
    coords = TurtleCanvas._canvas.coords(blot_id)
    assert coords == [_scale_x(TurtleCanvas._x - r), _scale_y(TurtleCanvas._y - r), _scale_x(TurtleCanvas._x + r), _scale_y(TurtleCanvas._y + r)]

def test_circle(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Draw a circle with radius r
    r = 10
    circle_id = circle(r)

    # Check that the circle was drawn
    assert circle_id in TurtleCanvas._canvas.find_all()

    # Check that the circle was drawn at the correct coordinates
    coords = TurtleCanvas._canvas.coords(circle_id)
    assert coords == [_scale_x(TurtleCanvas._x - r), _scale_y(TurtleCanvas._y - r), _scale_x(TurtleCanvas._x + r), _scale_y(TurtleCanvas._y + r)]

def test_ellipse(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Draw an ellipse with major, minor axes a, b
    a, b = 20, 10
    ellipse_id = ellipse(a, b)

    # Check that the ellipse was drawn
    assert ellipse_id in TurtleCanvas._canvas.find_all()

    # Check that the ellipse was drawn at the correct coordinates
    coords = TurtleCanvas._canvas.coords(ellipse_id)
    assert coords == [_scale_x(TurtleCanvas._x - a), _scale_y(TurtleCanvas._y - b), _scale_x(TurtleCanvas._x + a), _scale_y(TurtleCanvas._y + b)]

def test_ellblot(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Draw an ellipse with major, minor axes a, b
    a, b = 20, 10
    ellblot_id = ellblot(a, b)

    # Check that the ellipse was drawn
    assert ellblot_id in TurtleCanvas._canvas.find_all()

    # Check that the ellipse was drawn at the correct coordinates
    coords = TurtleCanvas._canvas.coords(ellblot_id)
    assert coords == [_scale_x(TurtleCanvas._x - a), _scale_y(TurtleCanvas._y - b), _scale_x(TurtleCanvas._x + a), _scale_y(TurtleCanvas._y + b)]
    
def test_pixset(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Set a pixel at (x, y) with colour c
    x, y, c = 10, 20, 'red'
    pixset_id = pixset(x, y, c)

    # Check that the pixel was drawn
    assert pixset_id in TurtleCanvas._canvas.find_all()

    # Check that the pixel was drawn at the correct coordinates
    coords = TurtleCanvas._canvas.coords(pixset_id)
    assert coords == [_scale_x(x), _scale_y(y), _scale_x(x + 1), _scale_y(y + 1)]

    # Check that the pixel was drawn with the correct colour
    assert TurtleCanvas._canvas.itemcget(pixset_id, 'fill') == c

def test_box(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Draw a box with width w, height h
    w, h = 10, 20
    box_id = box(w, h, 'blue', True)

    # Check that the box was drawn
    assert box_id in TurtleCanvas._canvas.find_all()

    # Check that the box was drawn at the correct coordinates
    coords = TurtleCanvas._canvas.coords(box_id)
    assert coords == [_scale_x(TurtleCanvas._x), _scale_y(TurtleCanvas._y), _scale_x(TurtleCanvas._x + w), _scale_y(TurtleCanvas._y + h)]

    # Check that the box was drawn with the correct colour
    assert TurtleCanvas._canvas.itemcget(box_id, 'fill') == 'blue'

def test_polygon(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Draw a polygon with vertices v
    hist = [(10, 20), (30, 40), (50, 60)]
    TurtleCanvas._history = hist

    polygon_id = polygon(3)

    # Check that the polygon was drawn
    assert polygon_id in TurtleCanvas._canvas.find_all()

    # Check that the polygon was drawn with the correct vertices
    coords = TurtleCanvas._canvas.coords(polygon_id)
    assert coords == [_scale_x(10), _scale_y(20), _scale_x(30), _scale_y(40), _scale_x(50), _scale_y(60)]

def test_polyline(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Draw a polyline with vertices v
    hist = [(10, 20), (30, 40), (50, 60)]
    TurtleCanvas._history = hist

    polyline_id = polyline(3)

    # Check that the polyline was drawn
    assert polyline_id in TurtleCanvas._canvas.find_all()

    # Check that the polyline was drawn with the correct vertices
    # (Polyline only returns the id of the last line segment)
    coords = TurtleCanvas._canvas.coords(polyline_id)
    assert coords == [_scale_x(30), _scale_y(40), _scale_x(50), _scale_y(60)]

def test_display(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Display text t
    t = 'Hello, World!'
    display_id = display(t)

    # Check that the text was displayed
    assert display_id in TurtleCanvas._canvas.find_all()

    # Check that the text was displayed at the correct coordinates
    coords = TurtleCanvas._canvas.coords(display_id)
    assert coords == [_scale_x(TurtleCanvas._x), _scale_y(TurtleCanvas._y)]

    # Check that the text was displayed with the correct text
    assert TurtleCanvas._canvas.itemcget(display_id, 'text') == t

def test_blank(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Draw a blank canvas
    blank_id = blank("white")

    # Check that the canvas was drawn
    assert blank_id in TurtleCanvas._canvas.find_all()

    # Check that the canvas was drawn with the correct colour
    assert TurtleCanvas._canvas.itemcget(blank_id, 'fill') == 'white'

    # Check that the coordinates of the canvas are (0, 0) to (width, height)
    coords = TurtleCanvas._canvas.coords(blank_id)
    assert coords == [0, 0, TurtleCanvas._width, TurtleCanvas._height]

def test_recolour(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Recolour area (x1, y1) to (x2, y2) with colour c
    x1, y1, x2, y2, c = 10, 20, 30, 40, 'blue'
    recolour_id = recolour(x1, y1, x2, y2, c)

    # Check that the area was recoloured
    assert recolour_id in TurtleCanvas._canvas.find_all()

    # Check that the area was recoloured with the correct colour
    assert TurtleCanvas._canvas.itemcget(recolour_id, 'fill') == c

    # Check that the area was recoloured at the correct coordinates
    coords = TurtleCanvas._canvas.coords(recolour_id)
    assert coords == [_scale_x(x1), _scale_y(y1), _scale_x(x2), _scale_y(y2)]

def test_fill(monkeypatch, tc_setup):
    # Monkey patch the pixcol function to save the input parameters and output white
    calls = []
    def pixcol_mock(x, y):
        calls.append((x, y))
        return 0xFFFFFF
    
    # Monkey patch the pixcol function
    monkeypatch.setattr(sys.modules['turtle_oxford'], 'pixcol', pixcol_mock)
    fill(10, 20, 'red')

    # Check that the pixcol function was called with the correct parameters
    assert calls == [(10, 20)]

def test_pixcol(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Set a pixel at (x, y) with colour c
    x, y, c = 10, 20, 'red'
    pixset_id = pixset(x, y, c)

    # Check the colour of the pixel at (x, y)
    assert pixcol(x, y) == 0xFF0000

    # Set the same pixel to a different colour
    pixset_id = pixset(x, y, 'blue')

    # Check the colour of the pixel at (x, y)
    assert pixcol(x, y) == 0x0000FF