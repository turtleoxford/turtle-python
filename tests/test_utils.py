import time
import math
import sys
import pytest
import tkinter
import os
from turtle_oxford import (TurtleCanvas, turtle_canvas) # Standard imports

# Lambda to check if two floats are close (avoiding floating point errors)
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

# Mock Event class to simulate keyboard/mouse events for input testing
class MockEvent:
    def __init__(self, event_type=tkinter.EventType.Key, keysym="a", keycode=65, x_root=100, y_root=200, num=1):
        self.type = event_type
        self.keysym = keysym
        self.keycode = keycode
        self.x_root = x_root
        self.y_root = y_root
        self.num = num  # For mouse button number

# Class that mocks the turtle canvas (for monkeypatching)
class FakeCanvas:
    def __init__(self):
        self.called = False
        
    def mainloop(self):
        # Simply record that mainloop was called
        self.called = True

# Fixture to create a temporary file for testing
@pytest.fixture
def temp_file(tmp_path):
    # Create a temporary file with some content
    file_path = tmp_path / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("line1\nline2\nline3")
    return str(file_path)