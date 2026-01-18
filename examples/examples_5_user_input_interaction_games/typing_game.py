import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # show instructions
    blank(cream)
    colour(black)
    setxy(15,200)
    display('In this typing test,  you will be shown the',"Arial",36)
    setxy(20,270)
    display('letters of the alphabet in a random order,',"Arial",36)
    setxy(20,340)
    display('and in a mixture of upper- and lower-case.',"Arial",36)
    setxy(20,410)
    display('Type them as fast as you can, and see how',"Arial",36)
    setxy(20,480)
    display('quickly you can finish the entire alphabet.',"Arial",36)
    setxy(20,620)
    display('Now wait 5 seconds or press "Esc" key to start ...',"Arial",30)
    keyecho(False)
    # wait for escape key, 5 seconds maximum, before proceeding...
    det=detect("Escape",5000)
    # create a string containing all letters of the alphabet}
    letters=''
    # choose a random first character
    c=randint(0, 25)
    # choose a random odd increment other than 13
    d=(randint(0, 11)*2+15)%26
    while len(letters)<26:
        # calculate next letter in sequence
        c=(c+d)%26
        # randomly select upper or lower case
        if randint(0, 1):
            letters=letters+chr(c+65)
        else:
            letters=letters+chr(c+97)
    # set timer to zero
    timeset(0)
    # for each letter in turn...
    for letter in letters:
        # rub out previous letter
        blank(black)
        # print letter at random coordinates
        setxy(randint(100,400),randint(0, 249))
        colour(yellow)
        display(letter,"Arial",450)
        # wait for user to type that letter
        while True:
            keys = read(1)
            if keys and keys[0] == letter:
                break
            if not keys:
                pause(10)
    # show time taken
    blank(lightblue)
    setxy(60,460)
    colour(lightred)
    display('Your time was '+qstr(time(),1000,2)+' seconds',"Arial",50)