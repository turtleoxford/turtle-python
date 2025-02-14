import time
import math
import sys
import pytest
import tkinter
import os
from turtle_oxford import (TurtleCanvas, turtle_canvas) # Standard imports
from turtle_oxford import (delete, pad, intdef, qstr, qint, qval) # Functions under testing
TclError = tkinter.TclError  # in case needed

def test_delete():
    # Delete 2 characters from the string 'Millican' starting at index 2 -> 'Miican'
    assert delete('Millican', 2, 2) == 'Miican'

def test_pad():
    # Pad the string 'Oxford' with 3 spaces to the right -> 'Oxford   '
    assert pad('Oxford', ' ', 9) == 'Oxford   '

def test_intdef():
    # Test intdef: intdef('3', 0) = 3, intdef('abc', 1) = 1
    assert intdef('3', 0) == 3
    assert intdef('abc', 1) == 1

def test_qstr():
    # qstr(1, 3, 5) -> "0.33333", qstr(1, 2, 3) -> "0.500"
    assert qstr(1, 3, 5) == "0.33333"
    assert qstr(1, 2, 3) == "0.500"

def test_qint():
    # qint("0.5", 3, 5) -> 2, qint("0.abc", 3, 5) -> 5
    assert qint("0.5", 3, 5) == 2
    assert qint("0.abc", 3, 5) == 5

def test_qval():
    # qval("0.5", 3, 5) -> 0.5, qval("0.abc", 3, 5) -> 0.5
    assert qval("0.5", 3, 5) == 0.5
    assert qval("0.abc", 3, 5) == 0.5