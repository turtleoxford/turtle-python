import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(1000, 1000) as t:
    decimals = 4 # decimal places for display of values
    # Using float-based functions from turtle_oxford; no denominator scaling

    # Writes to the output the value of a mathematical function of a/b,
    # or - in the case of HYPOT (where OP is "," not "/") - of a and b;
    def show(fn,op,value,degrees):
        vstr = f"{value:.{decimals}f}"
        if degrees==1:
            print(fn+'('+str(a)+op+str(b)+') = '+vstr)
        elif degrees==2:
            print(fn+'('+str(a)+op+str(b)+') = '+vstr)
        else:
            print(fn+'('+str(a)+op+str(b)+') = '+vstr)

    # show output and display information about the program
    print('This program selects two random numbers a and b, in the range')
    print('100-999, and then outputs various mathematical functions of the')
    print('fraction a/b. The results are expressed to '+str(decimals)+' decimal places.')
    print('')
    # set a and b to random values, and display their values and quotient
    a=randint(100,999)
    b=randint(100,999)
    print('a = '+str(a)+' b = '+str(b))
    print('a / b = '+str(a)+' / '+str(b)+' = '+qstr(a,b,decimals))
    print('')
    # display square, square root, cube, and cube root of a/b (float API)
    ratio = a / b
    show('square','/',power(ratio,2),0)
    show('square root','/',root(ratio,2),0)
    show('cube','/',power(ratio,3),0)
    show('cube root','/',root(ratio,3),0)
    print('')
    # display hypotenuse of right-angled triangle with shorter sides a and b
    show('hypot',',',hypot(a,b),0)
    show('calculated hypot',',',root(a*a+b*b,2),0)
    print('')
    # display sin, cos, and tan of a/b, interpreted in degrees
    show('sin','/',sin(ratio),1)
    show('cos','/',cos(ratio),1)
    show('tan','/',tan(ratio),1)
    print('')
    # display ln, exp, log10, and antilog of a/b
    show('ln','/',log(ratio),0)
    show('exp','/',exp(ratio),0)
    show('log10','/',log10(ratio),0)
    # antilog in float API is 10**x; use log10 inverse
    show('antilog','/',power(10, log10(ratio)),0)
    print('')
    # display arccos, arcsin, and arctan of a/b, in degrees
    if ratio>1:
        print('ARCCOS and ARCSIN are not defined for '+str(a)+'/'+str(b)+' = '+qstr(a,b,decimals))
    else:
        show('arccos','/',acos(ratio),2)
        show('arcsin','/',asin(ratio),2)
    show('arctan','/',atan(ratio),2)