API Reference
=============

This section documents all public functions in the Turtle Python library.

.. currentmodule:: turtle_oxford

Canvas Setup
------------

Functions for initialising and managing the canvas.

.. autofunction:: turtle_canvas
.. autofunction:: canvas
.. autofunction:: update
.. autofunction:: noupdate

Movement & Position
-------------------

Functions for moving the turtle and setting its position.

.. autofunction:: forward
.. autofunction:: back
.. autofunction:: home
.. autofunction:: setx
.. autofunction:: sety
.. autofunction:: setxy
.. autofunction:: movexy
.. autofunction:: drawxy
.. autofunction:: turtx
.. autofunction:: turty

Direction
---------

Functions for controlling the turtle's direction.

.. autofunction:: right
.. autofunction:: left
.. autofunction:: direction
.. autofunction:: angles
.. autofunction:: turnxy

Drawing Shapes
--------------

Functions for drawing various shapes.

.. autofunction:: circle
.. autofunction:: ellipse
.. autofunction:: blot
.. autofunction:: ellblot
.. autofunction:: box
.. autofunction:: polygon
.. autofunction:: polyline
.. autofunction:: display
.. autofunction:: blank
.. autofunction:: fill
.. autofunction:: pixset
.. autofunction:: pixcol

Pen Control
-----------

Functions for controlling the pen.

.. autofunction:: penup
.. autofunction:: pendown
.. autofunction:: thickness
.. autofunction:: colour
.. autofunction:: colour_to_int
.. autofunction:: colour_to_str

State Management
----------------

Functions for managing turtle history.

.. autofunction:: remember
.. autofunction:: forget

User Input & Events
-------------------

Functions for handling keyboard and mouse input.

.. autofunction:: detect
.. autofunction:: status
.. autofunction:: reset
.. autofunction:: get_key_code
.. autofunction:: get_key_sym
.. autofunction:: get_click
.. autofunction:: get_clickx
.. autofunction:: get_clicky
.. autofunction:: get_mousex
.. autofunction:: get_mousey
.. autofunction:: get_lmouse
.. autofunction:: get_rmouse
.. autofunction:: on_press
.. autofunction:: on_release
.. autofunction:: on_move
.. autofunction:: keybuffer
.. autofunction:: keyecho
.. autofunction:: read

Changing Turtles
-----------------

Functions for changing the current turtle.

.. autofunction:: new_turtle
.. autofunction:: old_turtle

Maths Functions
--------------

Mathematical functions for calculations.

.. autofunction:: cos
.. autofunction:: sin
.. autofunction:: tan
.. autofunction:: acos
.. autofunction:: asin
.. autofunction:: atan
.. autofunction:: exp
.. autofunction:: log
.. autofunction:: log10
.. autofunction:: power
.. autofunction:: sqrt
.. autofunction:: hypot
.. autofunction:: pi
.. autofunction:: sign
.. autofunction:: root

Colour Utilities
---------------

Functions for working with colours.

.. autofunction:: randcol
.. autofunction:: rgb
.. autofunction:: mixcols
.. autofunction:: recolour

String Functions
----------------

Functions for string manipulation.

.. autofunction:: delete
.. autofunction:: pad
.. autofunction:: intdef
.. autofunction:: qstr
.. autofunction:: qint
.. autofunction:: qval

Numeric Utilities
-----------------

Utility functions for number operations.

.. autofunction:: divmult
.. autofunction:: maxint
.. autofunction:: antilog
.. autofunction:: randint
.. autofunction:: randrange
.. autofunction:: randseed

File Operations
---------------

Functions for file input/output.

.. autofunction:: fopen
.. autofunction:: fclose
.. autofunction:: fread
.. autofunction:: freadline
.. autofunction:: fwrite
.. autofunction:: fwriteline
.. autofunction:: fmove
.. autofunction:: frename
.. autofunction:: fremove
.. autofunction:: frestart
.. autofunction:: fexists
.. autofunction:: fcopy
.. autofunction:: eof
.. autofunction:: eoln

Directory Operations
--------------------

Functions for directory management.

.. autofunction:: chdir
.. autofunction:: mkdir
.. autofunction:: rmdir
.. autofunction:: mkfile
.. autofunction:: isdir
.. autofunction:: isfile
.. autofunction:: checkdir
.. autofunction:: checkfile
.. autofunction:: finddir
.. autofunction:: findfirst
.. autofunction:: findnext

System Functions
----------------

System-level functions.

.. autofunction:: console
.. autofunction:: time
.. autofunction:: timeset
.. autofunction:: pause
.. autofunction:: halt

Constants Module
----------------

The colours and other constants used throughout the library are given in the :mod:`constants` module.
