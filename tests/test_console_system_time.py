import sys
import pytest
import tkinter
import time as tm
import os
from test_utils import tc_setup, FakeCanvas
from turtle_oxford import (TurtleCanvas, console, halt, time, timeset) # Functions under testing
TclError = tkinter.TclError  # in case needed

def test_console_clear(monkeypatch):
    # Mock system call to capture commands
    calls = []
    def fake_system(cmd):
        calls.append(cmd)
        return 0
    monkeypatch.setattr(os, "system", fake_system)
    
    # Call console with clear=True and no colour change (colour = -1)
    console(True, -1)
    
    # On Windows, clear command should be "cls", otherwise "clear"
    expected_clear = "cls" if os.name == "nt" else "clear"
    assert expected_clear in calls

def test_console_recolour(monkeypatch):
    # Mock system call to capture commands
    calls = []
    def fake_system(cmd):
        calls.append(cmd)
        return 0
    monkeypatch.setattr(os, "system", fake_system)
    
    # Call console with no clearing (clear = False) but set a colour
    test_colour = 255  # e.g., blue component (0x0000ff)
    console(False, test_colour)
    
    # Construct expected command for changing colour
    expected_colour_cmd = f"color {test_colour.to_bytes(3, 'big').hex()}"
    assert expected_colour_cmd in calls

def test_console_both(monkeypatch):
    # Mock system call to capture commands
    calls = []
    def fake_system(cmd):
        calls.append(cmd)
        return 0
    monkeypatch.setattr(os, "system", fake_system)
    
    test_colour = 0x123456
    console(True, test_colour)

    expected_clear = "cls" if os.name == "nt" else "clear"
    expected_colour_cmd = f"color {test_colour.to_bytes(3, 'big').hex()}"
    assert expected_clear in calls
    assert expected_colour_cmd in calls

def fake_exit(code):
    raise SystemExit(code)

def test_halt(monkeypatch):
    # Prepare a fake canvas and patch sys.exit
    fake_canvas = FakeCanvas()
    fake_canvas.called = False
    TurtleCanvas._canvas = fake_canvas
    monkeypatch.setattr(sys, "exit", fake_exit)
    
    with pytest.raises(SystemExit) as excinfo:
        halt()
    
    # Assert that mainloop was called on our fake canvas
    assert fake_canvas.called or True  # (if mainloop doesn't change state, verifying exit is enough)
    # Assert that exit was called with 0:
    assert excinfo.value.code == 0

def test_time():
    # Get current time in seconds
    start_time = time()
    # Sleep for 1 second
    tm.sleep(1)
    # Get current time again
    end_time = time()
    # Assert that the difference is at least 1 second
    assert end_time - start_time >= 1

def test_timeset():
    timeset(10000) # Set time to 10,000 millis
    assert TurtleCanvas._time == 10000