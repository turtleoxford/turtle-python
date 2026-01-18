import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(1000, 1000) as t:
    print('Illustration of built-in list operations')
    print('\nList multiplication with [0]*8:')
    mylist=[0]*8
    print(mylist)
    print('\nAssignment of values to elements - square of index:')
    for index in range(8):
        mylist[index]=index*index
    print(mylist)
    print('\nAPPEND element valued 64 to the list:')
    mylist.append(64)
    print(mylist)
    print('\nDELETE element at index 3 from the list:')
    del mylist[3]
    print(mylist)
    print('\nEXTEND list with [81,100]:')
    mylist.extend([81,100])
    print(mylist)
    print('\nREMOVE element valued 16:')
    mylist.remove(16)
    print(mylist)
    print('\nIdentify INDEX of element valued 36:')
    index=mylist.index(36)
    print('Index of 36 =',index)
    print('\nINSERT element valued 16 at index 5:')
    mylist.insert(5,16)
    print(mylist)
    print('\nREVERSE list:')
    mylist.reverse()
    print(mylist)
    print('\nIterate through list elements:')
    for element in mylist:
        print(element, end='  ')
    print('\n\nPrint every third element:')
    for i in range(len(mylist)):
        if i%3==2:
            print(mylist[i], end='  ')