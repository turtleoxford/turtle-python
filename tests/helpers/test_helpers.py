import time
import math
import sys
import pytest
import tkinter
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_utils import tc_setup

from turtle_oxford import (TurtleCanvas, _scale_x, _scale_y, _degs_to_angle_units, _draw_line, _oval, _find_dirs_files) # Functions under testing
TclError = tkinter.TclError  # in case needed

def test_scale_functions(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 100
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Test _scale_x: (150 - 100) * 2 = 100, (200 - 100) * 2 = 200
    assert _scale_x(150) == 100
    assert _scale_x(200) == 200

    # Test _scale_y: (150 - 50) * 3 = 300, (200 - 50) * 3 = 450
    assert _scale_y(150) == 300
    assert _scale_y(200) == 450

def test_degs_to_angle_units():
    # Setup nonstandard angle units for testing
    TurtleCanvas._angles = 720

    # Test _degs_to_angle_units: 90 * 720 / 360 = 180, 180 * 720 / 360 = 360
    assert _degs_to_angle_units(90) == 180
    assert _degs_to_angle_units(180) == 360

def test_draw_line(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Draw a line from (150, 200) to (150, 200)
    line_id = _draw_line(150, 200, 200, 250)

    # Check that the line was drawn
    assert line_id in TurtleCanvas._canvas.find_all()

    # Check that the line was drawn at the correct coordinates
    coords = TurtleCanvas._canvas.coords(line_id)

    # Check that the line was drawn at the correct coordinates
    assert coords == [_scale_x(150), _scale_y(200), _scale_x(200), _scale_y(250)]

def test_oval(tc_setup):
    # Setup known values for scaling
    TurtleCanvas._origin_x = 50
    TurtleCanvas._origin_y = 50
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 3

    # Draw an oval with xradius 50, yradius 50, border True
    xradius = 50
    yradius = 50
    oval_id = _oval(50, 50, True)

    # Check that the oval was drawn
    assert oval_id in TurtleCanvas._canvas.find_all()

    # Check that the oval was drawn at the correct coordinates
    coords = TurtleCanvas._canvas.coords(oval_id)

    # Check that the oval was drawn at the correct coordinates
    assert coords == [_scale_x(TurtleCanvas._x - xradius), _scale_y(TurtleCanvas._y - yradius), _scale_x(TurtleCanvas._x + xradius), _scale_y(TurtleCanvas._y + yradius)]

def test_find_dirs_files():
    # Test that the function returns the correct values
    # Pattern is all files and dirs matching 'test_1' in the current directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pattern = os.path.join(base_dir, 'test_1*')
    dirsfiles = _find_dirs_files(pattern)
    print(dirsfiles)
    assert dirsfiles == [os.path.join(base_dir, 'test_1'), os.path.join(base_dir, 'test_1.txt')]