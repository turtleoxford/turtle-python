#!/bin/python3
from turtle_oxford import *

with turtle_canvas() as t:
    update()
    s: str = ""
    blank(0xFFFDD0)
    while s != "Escape":
        blank(0xFFFDD0)
        display(get_key_code())
    blank(0xFFFDD0)
    display("Done")
