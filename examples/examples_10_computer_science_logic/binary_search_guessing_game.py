import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from turtle_oxford import *

with turtle_canvas(600, 600) as t:
    canvas(0,0,1000,1000)
    lowest=1
    highest=1000
    print("Please choose a number between",lowest,"and",highest)
    pause(1000)
    print("Then after each guess, type C/H/L to indicate Correct/High/Low\n")
    pause(1000)
    while lowest<highest:
        middle=(lowest+highest)//2
        print("I guess",middle, end="    ")
        typed="A"
        while not(typed in ["C","H","L"]):
            typed=input().strip().upper()
        if typed=="C":
            break
        elif typed=="H":
            print("MY GUESS WAS TOO HIGH", end=" ")
            highest=middle-1
        elif typed=="L":
            print("MY GUESS WAS TOO LOW", end=" ")
            lowest=middle+1
        print("(range is now ",lowest,"-",highest,")\n",sep="")
    if typed=="C":
        print("SUCCESS!")
    elif lowest==highest:
        print("Your number must be",lowest)
    else:
        print("Impossible!")