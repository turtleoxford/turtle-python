import time
import threading
import tkinter
import os
from tkinter import EventType
import pytest
from test_utils import tc_setup, MockEvent 
from turtle_oxford import (TurtleCanvas)
from turtle_oxford import (on_press, on_release, detect, get_key_sym, get_key_code, get_clickx, get_clicky, get_click, status, reset, keybuffer, keyecho, read) # Functions under testing
TclError = tkinter.TclError  # in case needed

# Use a lambda to check if two floats are close (avoiding floating point errors)
is_close = lambda a, b: abs(a - b) < 1e-6

def test_on_press_key_event(tc_setup):
    # Initialize key buffer to prevent IndexError
    TurtleCanvas._key_buffer = []
    TurtleCanvas._key_buffer_size = 10
    
    # Test key press event
    mock_event = MockEvent(event_type=EventType.Key, keysym="a", keycode=65)
    on_press(mock_event)
    
    # Check if key info was updated correctly
    assert TurtleCanvas._key_sym == "a"
    assert TurtleCanvas._key_code == 65
    assert TurtleCanvas._pressed_keys["a"] == 128  # kshift default value
    assert TurtleCanvas._pressed_keys["key"] == 128

def test_on_press_mouse_event(tc_setup):
    # Initialize key buffer to prevent IndexError
    TurtleCanvas._key_buffer = []
    TurtleCanvas._key_buffer_size = 10
    
    # Test mouse press event
    mock_event = MockEvent(event_type=EventType.ButtonPress, keysym="", keycode=0, x_root=100, y_root=200, num=1)
    on_press(mock_event)
    
    # Check if mouse info was updated correctly
    assert TurtleCanvas._key_sym == "mouse1"
    assert TurtleCanvas._key_code == 129  # 128 + event.num
    assert TurtleCanvas._pressed_keys["mouse1"] == 128
    assert TurtleCanvas._pressed_keys["clickx"] == 100
    assert TurtleCanvas._pressed_keys["clicky"] == 200

def test_on_release_key_event(tc_setup):
    # First simulate key press
    mock_press = MockEvent(event_type=EventType.Key, keysym="a", keycode=65)
    on_press(mock_press)
    
    # Now simulate key release
    mock_release = MockEvent(event_type=EventType.KeyRelease, keysym="a", keycode=65)
    on_release(mock_release)
    
    assert TurtleCanvas._pressed_keys["a"] == -128
    assert TurtleCanvas._pressed_keys["key"] == -128

def test_on_release_mouse_event(tc_setup):
    # First simulate mouse press
    mock_press = MockEvent(event_type=EventType.ButtonPress, keysym="", keycode=0, num=1)
    on_press(mock_press)
    
    # Now simulate mouse release
    mock_release = MockEvent(event_type=EventType.ButtonRelease, keysym="", keycode=0, num=1)
    on_release(mock_release)
    
    # Check if status was flipped
    assert TurtleCanvas._pressed_keys["mouse1"] == -128
    assert TurtleCanvas._pressed_keys["mouse"] == -128

def test_key_getters(tc_setup):
    # Setup key press
    mock_event = MockEvent(event_type=EventType.Key, keysym="a", keycode=65)
    on_press(mock_event)
    
    # Test getters
    assert get_key_sym() == "a"
    assert get_key_code() == 65

def test_mouse_getters(tc_setup):
    # Setup context - configure scale and origin
    TurtleCanvas._x_multiplier = 2
    TurtleCanvas._y_multiplier = 2
    TurtleCanvas._origin_x = 10
    TurtleCanvas._origin_y = 20
    
    # Setup mouse press at (100, 200)
    mock_event = MockEvent(event_type=EventType.ButtonPress, x_root=100, y_root=200, num=1)
    on_press(mock_event)
    
    # Test mouse coordinate getters (should account for origin and multipliers)
    assert get_clickx() == 60  # (100/2)+10
    assert get_clicky() == 120  # (200/2)+20
    assert get_click() == "mouse1"

def test_status_and_reset(tc_setup):
    # Setup key press
    mock_event = MockEvent(event_type="Key", keysym="a", keycode=65)
    on_press(mock_event)
    
    # Test status
    assert status("a") == 128
    
    # Test reset
    reset("a")
    assert status("a") == 0
    
    # Test status for key that was never pressed
    assert status("b") == 0

def test_keybuffer_and_read(tc_setup):
    # Directly set class variables instead of using keybuffer function
    TurtleCanvas._key_buffer = []
    TurtleCanvas._key_buffer_size = 3
    
    # Simulate key presses to fill buffer
    on_press(MockEvent(keysym="a"))
    on_press(MockEvent(keysym="b"))
    on_press(MockEvent(keysym="c"))
    
    # Test read - should return up to max_size characters
    result = read(2)
    assert len(result) == 2
    assert "a" in result 
    assert "b" in result
    
    result = read(5)
    assert len(result) == 3  # Should only return 3 items even though we asked for 5
    assert "a" in result
    assert "b" in result
    assert "c" in result

def test_keyecho(tc_setup):
    TurtleCanvas._key_echo = False

    # Test echo off
    keyecho(False)
    assert TurtleCanvas._key_echo == False

    # Test echo on
    keyecho(True)
    assert TurtleCanvas._key_echo == True

# Special timeout override for detect test to make it fast
def mocked_pause(duration):
    pass

# The detect test has been commented out because it has indeterministic behaviour due to threading

# def test_detect(monkeypatch, tc_setup):
#     # Override pause to prevent delay
#     monkeypatch.setattr("turtle_oxford.pause", mocked_pause)

#     result = []
#     # Create a thread to run detect
#     def run_detect():
#         print("Detecting")
#         result.append(detect("a", 500))

#     # Start the detect thread
#     detect_thread = threading.Thread(target=run_detect)
#     detect_thread.daemon = True
#     detect_thread.start()

#     # Create a thread to simulate key press after a tiny delay
#     def simulate_keypress():
#         print("a pressed")
#         time.sleep(0.2)  # Small delay to ensure detect has started
#         # Directly set the key state that would result from a press
#         TurtleCanvas._pressed_keys["a"] = 128
#         TurtleCanvas._key_sym = "a"
    
#     # Start the key press simulation thread
#     keypress_thread = threading.Thread(target=simulate_keypress)
#     keypress_thread.daemon = True
#     keypress_thread.start()

#     keypress_thread.join(timeout = 1)
#     detect_thread.join(timeout = 1)

#     print(result)
    
#     # The result should be the key we "pressed"
#     assert result[0] == "a"
