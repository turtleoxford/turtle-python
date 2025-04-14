import sys
import pytest
import tkinter
from test_utils import tc_setup
from constants import *
from turtle_oxford import (TurtleCanvas, randcol, rgb, mixcols, randint, randrange, randseed) # Functions under testing
TclError = tkinter.TclError  # in case needed

def test_randcol(tc_setup):
    assert randcol(colour_list.__len__()) in colour_list

def test_rgb(tc_setup):
    # Green
    assert rgb(0) == 0x228B22

    # Red
    assert rgb(1) == 0xFF0000

def test_mixcols(tc_setup):
    # Test mixcols: (10 * 2 + 20 * 5)//7 = 16
    assert mixcols(10, 20, 2, 5) == 17

def test_randint(tc_setup):
    # Test randint: 5 <= randint(5, 10) < 10
    assert 5 <= randint(5, 10) <= 10

def test_randrange(tc_setup):
    # Test randrange: 0 <= randrange(5) < 5
    assert 0 <= randrange(5) <= 5

def test_randseed(tc_setup):
    # Test randseed: randseed(1) => seed = 1
    randseed(1)
    # Cannot check seed value, but should not raise an exception