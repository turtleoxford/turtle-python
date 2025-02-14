import time
import math
import sys
import pytest
import tkinter
import os
from turtle_oxford import (TurtleCanvas, turtle_canvas) # Standard imports
from turtle_oxford import (_degs_to_angle_units) # Useful helpers
from turtle_oxford import (update, noupdate, canvas) # Functions under testing
TclError = tkinter.TclError  # in case needed

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

def test_update(tc_setup):
    update()
    assert TurtleCanvas._update

def test_noupdate(tc_setup):
    noupdate()
    assert not TurtleCanvas._update

def test_canvas(tc_setup):
    canvas(50, 50, 100, 100)

    # Check if multipliers are set correctly
    TurtleCanvas._x_multiplier = TurtleCanvas._width / 100
    TurtleCanvas._y_multiplier = TurtleCanvas._height / 100