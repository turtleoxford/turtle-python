import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(1000, 1000) as t:
    s=input('What is your name?  ')
    print('')
    print('Hello, '+s+', ...')
    pause(500)
    print('How are you?')