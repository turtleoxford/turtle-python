import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(1000, 1000) as t:
    delay = 500

    # set initial string
    s1='Turtle Python'
    # illustrate use of SLICE function
    s2=s1[0:6]
    print(s2+' is the name of a small animal.')
    pause(delay)
    s3=s1[7:13]
    print(s3+' is a large snake.')
    pause(delay)
    # illustrate insertion of one string into another
    s4=s3[0:1]+'onty M'+s3[1:len(s3)]
    print('\''+s4+'\' is a silly name.')
    pause(delay)
    # illustrate use of LEN function
    print('"'+s1+'" has '+str(len(s1))+' characters.')
    pause(delay)
    # illustrate use of LOWER and UPPER functions·
    print('In lower case it is "'+s1.lower()+'".')
    print('In upper case it is "'+s1.upper()+'".')
    pause(delay)
    posn=s1.find(s3)
    if posn>0:
        print('"'+s3+'" occurs within "'+s1+'" at position '+str(posn)+'.')
    pause(delay)
    s5='3.14159'
    print(s5+' times 100000 = '+str(qint(s5,100000,-1))+'.')
    pause(delay)
    n=qint(s5,100000,-1)
    print(str(n)+' divided by 100000 = '+qstr(n,100000,5)+'.')
    print('')
    pause(delay*5)
    print('Now back to the Canvas and Console ...')
    output(False,peach,True)
    pause(delay*5)
    output(False,lightred,False)
    pause(delay*5)
    console(True,lightblue)
    print('You will see this on a clear light blue Console')