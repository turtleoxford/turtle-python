Quick Start Guide
=================

Basic Usage
-----------

All Turtle Python programs follow this basic structure:

.. code-block:: python

   from turtle_oxford import *

   with turtle_canvas(width, height) as t:
       # Your drawing code here
       forward(100)
       right(90)
       blot(50)

The ``turtle_canvas()`` context manager ensures proper initialisation and cleanup.

Drawing Shapes
--------------

.. code-block:: python

   from turtle_oxford import *

   with turtle_canvas(500, 500) as t:
       # Draw a square
       for i in range(4):
           forward(100)
           right(90)


Colours and Styles
-----------------

Turtle Python supports multiple colour formats:

.. code-block:: python

   from turtle_oxford import *

   with turtle_canvas(500, 500) as t:
       # Using predefined colours
       colour("red")
       
       # Using RGB tuple
       colour((255, 128, 0))
       
       # Using hex integer
       colour(0xFF8000)
       
       # Adjust pen thickness
       thickness(5)

Movement
--------

.. code-block:: python

   from turtle_oxford import *

   with turtle_canvas(500, 500):
       # Relative movement
       forward(100)
       back(50)
       
       # Absolute positioning
       setxy(100, 100)
       
       # Relative positioning
       movexy(50, -25)
       
       # Pen control
       penup()
       forward(50)  # Move without drawing
       pendown()

User Input
----------

.. code-block:: python

   from turtle_oxford import *

   with turtle_canvas(500, 500):
       # Ask for typed input
       name = input("Enter your name: ")

       # Detect a mouse click within 5 seconds
       print("Click anywhere within 5 seconds...")
       mk = detect("mousekey", 5000)
       
       # Check specific key
       if mk == "mouse1":
           print("Left mouse button clicked!")
       elif mk == "mouse2":
           print("Middle mouse button clicked!")
       elif mk == "mouse3":
           print("Right mouse button clicked!")

Next Steps
----------

* Explore the :doc:`api` for complete function reference.
* Check out :doc:`examples` for more complex programs.
* Read the source code for implementation details.
