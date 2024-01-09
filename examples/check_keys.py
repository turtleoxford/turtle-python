import time
from turtle_oxford import *
from random import randrange, randint

with turtle_canvas(0, 0, 1000, 1000) as t:
    # show instructions}
    blank(0xFFFDD0)
    setxy(15, 200)
    colour("black")
    display("In this typing test, you will be shown the", "Helvetica", 32)
    setxy(20, 270)
    display("letters of the alphabet in a random order,", "Helvetica", 32)
    setxy(20, 340)
    display("and in a mixture of upper- and lower-case.", "Helvetica", 32)
    setxy(20, 410)
    display("Type them as fast as you can, and see how", "Helvetica", 32)
    setxy(20, 480)
    display("quickly you can finish the entire alphabet.", "Helvetica", 32)
    setxy(20, 620)
    display('Now wait 5 seconds or press "Esc" key to start ...', "Helvetica", 32)
    # wait for escape key, 5 seconds maximum, before proceeding...
    det = detect("Escape", 5000)
    # create a string containing all letters of the alphabet
    letters = ""
    # choose a random first character
    c = randrange(26)
    # choose a random odd increment other than 13
    d: int = (randrange(12) * 2 + 15) % 26
    while len(letters) < 26:
        # calculate next letter in sequence
        c = (c + d) % 26
        letters = letters + chr(c + 65)
    # set timer to zero
    start_time = time.time()
    # for each letter in turn...
    for letter in letters:
        # get character code of that letter
        c = ord(letter)
        # select case at random
        lowercase = randrange(2)
        # rub out previous letter
        blank("black")
        # print letter at random coordinates
        setxy(randint(100, 400), randrange(250))
        colour("yellow")
        # print in either lowercase or uppercase
        displayed_letter = chr(c + 32 * lowercase)
        display(displayed_letter, 3, 450)
        display(displayed_letter, 3, 450)
        # wait for user to type that letter, with shift down for uppercase
        shiftok = False
        forget_key(letter)
        forget_key("Shift")
        if not lowercase:
            detect("Shift", 0)
        detect(displayed_letter, 0)
    # show time taken
    blank("blue")
    setxy(60, 460)
    colour("red")
    display("Your time was " + str(time.time() - start_time) + " seconds", 4, 50)
