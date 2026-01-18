import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(1000, 1000) as t:
    # calculates n! recursively - both the
    # parameter n and the result are integers
    def factorial(n):
        if n==0:
            return 1
        else:
            return n*factorial(n-1)

    # calculate and display n! for n = 1 to 10
    for count in range(1,11,1):
        print(str(count)+'! = '+str(factorial(count)))