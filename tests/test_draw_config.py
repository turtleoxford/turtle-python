import time
import math
import sys
import pytest
import tkinter
from PIL import ImageColor
import os
from test_utils import tc_setup
from turtle_oxford import (TurtleCanvas, colour_to_int, colour_to_str, colour, thickness, penup, pendown) # Functions under testing
TclError = tkinter.TclError  # in case needed

def test_colour_to_int_with_int():
    # When an int is provided it should return itself.
    assert colour_to_int(123) == 123

def test_colour_to_int_with_tuple():
    # Check conversion for an RGB tuple.
    rgb_tuple = (10, 20, 30)
    expected = (10 << 16) + (20 << 8) + 30
    assert colour_to_int(rgb_tuple) == expected

def test_colour_to_int_with_str():
    # For string inputs (e.g., "red"), ImageColor.getrgb is used.
    rgb = ImageColor.getrgb("red")
    expected = (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]
    assert colour_to_int("red") == expected

def test_colour_to_int_with_invalid_type():
    # If an unsupported type is passed (e.g., float), None should be returned.
    assert colour_to_int(3.14) is None

def test_colour_to_str_with_str():
    # If given a string, the function should return it unchanged.
    assert colour_to_str("blue") == "blue"

def test_colour_to_str_with_tuple():
    # For (16, 32, 48) -> "#102030"
    assert colour_to_str((16, 32, 48)) == "#102030"
    
    # For (255, 0, 0) -> "#ff0000"
    assert colour_to_str((255, 0, 0)) == "#ff0000"

def test_colour_to_str_with_int():
    # 255 -> "#0000ff"
    assert colour_to_str(255) == "#0000ff"

def test_colour(tc_setup):
    # Test colour: set colour to "red"
    colour("red")
    assert TurtleCanvas._colour == "red"

def test_thickness(tc_setup):
    # Test thickness: set thickness to 5
    thickness(5)
    assert TurtleCanvas._thick == 5

def test_penup(tc_setup):
    # Test penup: set pen to up
    penup()
    assert TurtleCanvas._pen == False

def test_pendown(tc_setup):
    # Test pendown: set pen to down
    pendown()
    assert TurtleCanvas._pen == True