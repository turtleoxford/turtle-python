import time
import math
import sys
import pytest
import tkinter
import os
from test_utils import tc_setup
from turtle_oxford import (TurtleCanvas, turtle_canvas) # Standard imports
from turtle_oxford import (remember, forget, new_turtle, old_turtle) # Functions under testing
TclError = tkinter.TclError  # in case needed

def test_remember(tc_setup):
    # Reset history
    TurtleCanvas._history = []

    # Set initial state
    TurtleCanvas._x = 0
    TurtleCanvas._y = 0

    # Remember the current state
    remember()

    # Move the turtle
    TurtleCanvas._x = 10
    TurtleCanvas._y = 10

    # Remember the new state
    remember()

    # Check if the history is correct
    assert TurtleCanvas._history == [(0, 0), (10, 10)]

def test_forget(tc_setup):
    # Set example history
    TurtleCanvas._history = [(0, 0), (10, 10), (20, 20), (30, 30)]

    # Forget the last state
    forget(1)

    # Check if the history is correct
    assert TurtleCanvas._history == [(0, 0), (10, 10), (20, 20)]

    # Forget the last two states
    forget(2)

    # Check if the history is correct
    assert TurtleCanvas._history == [(0, 0)]

def test_new_turtle(tc_setup):
    # Create a new turtle
    new_turtle([
        0, # x
        0, # y
        1, # direction
        10, # thickness
        0, # color
    ])

    # Check if attributes are set correctly
    assert TurtleCanvas._x == 0
    assert TurtleCanvas._y == 0
    assert TurtleCanvas._direction == 1
    assert TurtleCanvas._thick == 10
    assert TurtleCanvas._colour == 0

def test_old_turtle(tc_setup):
    # Set initial attributes
    TurtleCanvas._x = 0
    TurtleCanvas._y = 0
    TurtleCanvas._direction = 1
    TurtleCanvas._thick = 10
    TurtleCanvas._colour = 0

    # Create a new turtle
    new_turtle([
        10, # x
        10, # y
        2, # direction
        20, # thickness
        1, # color
    ])

    # Restore the old turtle
    old_turtle()

    # Check if attributes are restored correctly
    assert TurtleCanvas._x == 0
    assert TurtleCanvas._y == 0
    assert TurtleCanvas._direction == 1
    assert TurtleCanvas._thick == 10
    assert TurtleCanvas._colour == 0