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

def test_update(tc_setup, monkeypatch):
    # Track if refresh is called
    refresh_called = False
    def mock_refresh():
        nonlocal refresh_called
        refresh_called = True
    monkeypatch.setattr(TurtleCanvas, "refresh", mock_refresh)
    
    # Call update which should trigger a refresh
    update()
    assert refresh_called, "update() should call TurtleCanvas.refresh()"

def test_noupdate(tc_setup):
    # Enable updates to establish baseline
    update()
    
    # Create a mock to track if refresh would be called
    original_refresh = TurtleCanvas.refresh
    refresh_count = 0
    
    def counted_refresh():
        nonlocal refresh_count
        refresh_count += 1
    
    TurtleCanvas.refresh = counted_refresh
    
    try:
        # Create a shape with updates enabled (should trigger refresh)
        TurtleCanvas._canvas.create_rectangle(10, 10, 20, 20, fill="red")
        refresh_count_before = refresh_count
        
        # Disable updates
        noupdate()
        
        # Create another shape (should not trigger refresh)
        TurtleCanvas._canvas.create_rectangle(30, 30, 40, 40, fill="blue")
        
        # Check behavior: refresh should not be called after noupdate
        assert refresh_count == refresh_count_before, "noupdate() should prevent refreshes on drawing operations"
        
        # Verify both shapes exist despite no refresh
        items = TurtleCanvas._canvas.find_all()
        assert len(items) == 2, "Shapes should be added to canvas even when updates are disabled"
    finally:
        # Restore original refresh method
        TurtleCanvas.refresh = original_refresh

def test_canvas(tc_setup):
    canvas(50, 50, 100, 100)

    # Check if multipliers are set correctly
    TurtleCanvas._x_multiplier = TurtleCanvas._width / 100
    TurtleCanvas._y_multiplier = TurtleCanvas._height / 100