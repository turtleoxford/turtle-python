import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    # specify number of values to be calculated
    lastnum=35
    fibSave=[1]*(lastnum+1)

    # calculates nth Fibonacci number recursively
    def fibRecursive(n):
        if (n==1) or (n==2):
            return 1
        else:
            return fibRecursive(n-1)+fibRecursive(n-2)

    # calculates nth Fibonacci number iteratively,
    # assuming the n-1 and n-2 values have already
    # been calculated and stored in fibSave list
    def fibIterative(n):
        if (n==1) or (n==2):
            fibSave[n]=1
        else:
            fibSave[n]=fibSave[n-1]+fibSave[n-2]
        return fibSave[n]

    # set up and show the output display
    # calculate 25 Fibonacci values recursively (slow)
    print('First, by recursion:')
    timeset(0)
    for count in range(1,lastnum+1):
        print('fib('+str(count)+') = '+str(fibRecursive(count)))
    print('Time taken: '+qstr(time(),1000,5)+' seconds')
    print()
    print('Then, by iteration:')
    timeset(0)
    for count in range(1,lastnum+1):
        print('fib('+str(count)+') = '+str(fibIterative(count)))
    print('Time taken: '+qstr(time(),1000,5)+' seconds')