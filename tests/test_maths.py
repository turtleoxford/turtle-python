import time
import math
import sys
import pytest
import tkinter
import os
from turtle_oxford import (TurtleCanvas, turtle_canvas) # Standard imports
from turtle_oxford import (divmult, maxint, antilog, cos, acos, sin, asin, tan, atan, exp, log, log10, power, sqrt, pi, hypot, root, sign) # Functions under testing
TclError = tkinter.TclError  # in case needed

# Use a lambda to check if two floats are close (avoiding floating point errors)
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

def test_divmult():
    # Test divmult: 2/3 * 6 = 4, 1/3 * 4 = 1
    assert is_close(divmult(2, 3, 6), 4)
    assert is_close(divmult(1, 3, 4), 1)

def test_maxint():
    assert is_close(maxint(), sys.maxsize)

def test_antilog():
    # Test antilog: 10^(8/4) * 5 = 500
    assert is_close(antilog(8, 4, 5), 500)

def test_cos(tc_setup):
    # Set nonstandard angle units
    TurtleCanvas._angles = 720
    # Test cos: cos(0) = 1, cos(360) = -1
    assert is_close(cos(0), 1)
    assert is_close(cos(360), -1)

def test_acos(tc_setup):
    # Set nonstandard angle units
    TurtleCanvas._angles = 720
    # Test acos: acos(1) = 0, acos(-1) = 360
    assert is_close(acos(1), 0)
    assert is_close(acos(-1), 360)

def test_sin(tc_setup):
    # Set nonstandard angle units
    TurtleCanvas._angles = 720
    # Test sin: sin(0) = 0, sin(360) = 1
    assert is_close(sin(0), 0)
    assert is_close(sin(360), 0)

def test_asin(tc_setup):
    # Set nonstandard angle units
    TurtleCanvas._angles = 720
    # Test asin: asin(0) = 0, asin(0.5) = 90
    assert is_close(asin(0), 0)
    assert is_close(asin(0.5), 60)

def test_tan(tc_setup):
    # Set nonstandard angle units
    TurtleCanvas._angles = 720
    # Test tan: tan(0) = 0, tan(360) = 0
    assert is_close(tan(0), 0)
    assert is_close(tan(360), 0)

def test_atan(tc_setup):
    # Set nonstandard angle units
    TurtleCanvas._angles = 720
    # Test atan: atan(0) = 0, atan(1) = 45
    assert is_close(atan(0), 0)
    assert is_close(atan(1), 90)

def test_exp():
    # Test exp: exp(0) = 1, exp(1) = e
    assert is_close(exp(0), 1)
    assert is_close(exp(1), math.e)

def test_log():
    # Test log: log(1) = 0, log(e) = 1
    assert is_close(log(1), 0)
    assert is_close(log(math.e), 1)

def test_log10():
    # Test log10: log10(1) = 0, log10(10) = 1
    assert is_close(log10(1), 0)
    assert is_close(log10(10), 1)

def test_power():
    # Test power: 2^3 = 8, 3^2 = 9
    assert is_close(power(2, 3), 8)
    assert is_close(power(3, 2), 9)

def test_sqrt():
    # Test sqrt: sqrt(4) = 2, sqrt(9) = 3
    assert is_close(sqrt(4), 2)
    assert is_close(sqrt(9), 3)

def test_pi():
    # Test pi: pi = 3.141592653589793
    assert is_close(pi(), math.pi)

def test_hypot():
    # Test hypot: hypot(3, 4) = 5, hypot(6, 8) = 10
    assert is_close(hypot(3, 4), 5)
    assert is_close(hypot(6, 8), 10)

def test_root():
    # Test root: 3-root of 27 = 3, 2-root of 16 = 4
    assert is_close(root(27, 3), 3)
    assert is_close(root(16, 2), 4)

def test_sign():
    # Test sign: sign(-3) = -1, sign(3) = 1
    assert sign(-3) == -1
    assert sign(3) == 1
