import time
import math
import sys
import pytest
import tkinter
from PIL import ImageColor
import os
from test_utils import tc_setup, is_close
from turtle_oxford import (_degs_to_angle_units, _scale_x, _scale_y) # Useful helpers
from turtle_oxford import (TurtleCanvas, home, setx, sety, setxy, right, left, direction, angles, turnxy, forward, back, movexy, drawxy) # Functions under testing
TclError = tkinter.TclError  # in case needed

def test_home(tc_setup):
    # Set position to (100, 200)
    TurtleCanvas._x = 100
    TurtleCanvas._y = 200

    # Test home: home() should move the turtle to the centre (250, 250)
    home()
    assert TurtleCanvas._x == 250
    assert TurtleCanvas._y == 250

def test_setx(tc_setup):
    # Set position to (100, 200)
    TurtleCanvas._x = 100
    TurtleCanvas._y = 200

    # Test setx: setx(300) should move the turtle to (300, 200)
    setx(300)
    assert TurtleCanvas._x == 300
    assert TurtleCanvas._y == 200

def test_sety(tc_setup):
    # Set position to (100, 200)
    TurtleCanvas._x = 100
    TurtleCanvas._y = 200

    # Test sety: sety(300) should move the turtle to (100, 300)
    sety(300)
    assert TurtleCanvas._x == 100
    assert TurtleCanvas._y == 300

def test_setxy(tc_setup):
    # Set position to (100, 200)
    TurtleCanvas._x = 100
    TurtleCanvas._y = 200

    # Test setxy: setxy(300, 400) should move the turtle to (300, 400)
    setxy(300, 400)
    assert TurtleCanvas._x == 300
    assert TurtleCanvas._y == 400

def test_right(tc_setup):
    # Set direction to 0
    TurtleCanvas._direction = 0

    # Test right: right(90) should set the direction to 270
    right(90)
    assert TurtleCanvas._direction == 270

def test_left(tc_setup):
    # Set direction to 0
    TurtleCanvas._direction = 0

    # Test left: left(90) should set the direction to 90
    left(90)
    assert TurtleCanvas._direction == 90

def test_direction(tc_setup):
    TurtleCanvas._angles = 360
    # Set direction to 90
    direction(90)

    # Test direction: direction should return 90
    assert TurtleCanvas._direction == 90

def test_angles(tc_setup):
    # Set angle units to 720
    angles(720)

    # Test angles: angles() should return 720
    assert TurtleCanvas._angles == 720

def test_turnxy(tc_setup):
    # Set direction to 0
    TurtleCanvas._direction = 0

    # Set position to (0, 0)
    TurtleCanvas._x = 0
    TurtleCanvas._y = 0

    # Test turnxy: turnxy(200, 200) should set the direction to 45
    turnxy(200, 200)
    assert TurtleCanvas._direction == 45

def test_forward(tc_setup):
    TurtleCanvas._angles = 360

    # Set position to (0, 0)
    TurtleCanvas._x = 0
    TurtleCanvas._y = 0

    # Set direction to 0
    TurtleCanvas._direction = 45

    # Test forward: forward(sqrt(2 * 50^2)) should move the turtle to (-50, 50)
    forwardid = forward((2 * 50**2)**0.5)
    assert is_close(TurtleCanvas._x, -50)
    assert is_close(TurtleCanvas._y, -50)

def test_back(tc_setup):
    # Set position to (100, 200)
    TurtleCanvas._x = 100
    TurtleCanvas._y = 200

    # Set direction to 0
    TurtleCanvas._direction = 0

    # Test back: back(100) should move the turtle to (100, 300)
    back(100)
    assert TurtleCanvas._x == 100
    assert TurtleCanvas._y == 300

def test_movexy(tc_setup):
    # Set position to (100, 200)
    TurtleCanvas._x = 100
    TurtleCanvas._y = 200

    # Test movexy: movexy(200, 300) should move the turtle to (300, 500)
    movexy(200, 300)
    assert TurtleCanvas._x == 300
    assert TurtleCanvas._y == 500

def test_drawxy(tc_setup):
    # Set position to (100, 200)
    TurtleCanvas._x = 100
    TurtleCanvas._y = 200

    # Test drawxy: drawxy(200, 300) should move the turtle to (300, 500)
    drawid = drawxy(200, 300)
    assert TurtleCanvas._x == 300
    assert TurtleCanvas._y == 500

    # Check coordinates of the drawn object
    assert drawid in TurtleCanvas._canvas.find_all()
    coords = TurtleCanvas._canvas.coords(drawid)
    assert coords == [_scale_x(100), _scale_y(200), _scale_x(300), _scale_y(500)]
