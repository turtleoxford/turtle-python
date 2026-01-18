import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    s = ''
    while str(intdef(s,0))!=s:
        print('CALCULATION OF APPROXIMATE SQUARE ROOTS, BY ITERATION')
        print()
        s=input('Which square root would you like to calculate? ')
    print()
    print()
    print('   guess    '+s+'/guess')
    square=int(s)*1000000
    guess=1000
    quotient=square//guess
    while (guess!=quotient) and (guess!=(guess+quotient)//2):
        quotient=square//guess
        print()
        print(pad(qstr(guess,1000,3),' ',8)+'   '+pad(qstr(quotient,1000,3),' ',8), end='')
        pause(2000)
        if guess==quotient:
            print()
        else:
            print(pad('  sum = ',' ',14)+pad(qstr(guess+quotient,1000,3),' ',-8), end='')
            print('  average = '+qstr((guess+quotient)//2,1000,3))
        guess=(guess+quotient)//2
    print()
    print()
    print('The square root of '+s+' is approximately '+qstr(guess,1000,3))