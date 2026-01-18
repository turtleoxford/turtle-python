import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0, 0, 1000, 1000)
    # disable key output in the console
    keyecho(False)
    # repeatedly...
    while (True):
        # rub out previous frame
        blank(white)
        setxy(50,20)
        colour(blue)
        display('Type in a starting integer (>1):',"Arial",36)
        setxy(800,20)
        colour(black)
        # while waiting for input of integer greater than 1...
        first=-1
        while (first<=1):
            # empty the keybuffer
            keybuffer(100)
            s = ""
            # print contents of keybuffer on canvas
            enter_pressed = False
            while not enter_pressed:
                box(200,60,white,False)
                
                # Read and accumulate
                new_input = read(10)
                for key in new_input:
                    if key == "Return":
                        enter_pressed = True
                        break
                    elif key == "BackSpace":
                        if len(s) > 0:
                            s = s[:-1]
                    elif len(key) == 1:
                        s += key
                
                display(s,"Arial",36)
                if not enter_pressed:
                    pause(100)
            
            # try to convert s to integer
            first=intdef(s,-1)
            
            # Wait for key release (any key)
            while get_key_code() > 0:
                pause(10)
            
        # set latest number to user's input
        latest=first
        # initialise count variable
        count=0
        # print first number in blue
        colour(blue)
        # until the sequence reaches 1...
        while (latest!=1):
            # print the latest number
            setxy((count%10)*100+20,(count//10)*45+300)
            display(str(latest),"Arial",24)
            # move to the next number in the sequence
            if (latest%2==0):
                latest=latest/2
            else:
                latest=3*latest+1
            # increment the count variable
            count=count+1
            # print subsequent numbers in green
            colour(green)
        # print const number (1) in red
        setxy((count%10)*100+20,(count//10)*45+300)
        colour(red)
        display(str(latest),"Arial",24)
        # print length of sequence
        setxy(100,100)
        display('That took '+str(count)+' iterations to reach 1',"Arial",36)
        colour(black)
        setxy(250,200)
        # wait for key press to start again
        display('[Press a key to continue]',"Arial",30)
        
        # Clear any buffered keys
        keybuffer(100)
        
        # Wait for a new key press
        while len(read(1)) == 0:
            pause(10)