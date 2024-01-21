Usage
=======

====================
Installing Python
====================

A good place to start is to consult the official Python starter documentation here: https://wiki.python.org/moin/BeginnersGuide.

First, you need to have both Python and pip installed. Some operating systems come with the former already pre-installed. To check if it is indeed installed,
you can run the following command in a shell (this is a terminal window on a Unix machine or a Command Prompt or PowerShell window on a Windows machine)::

    python --version

If the version is too old (starts with 2.X), then you need to follow the installation steps anyway.

To install Python, please go to https://www.python.org/downloads/ where you can download a Python installer. If you're having any issues or questions related to
the installer, you should consult this installation guide which has information for most operating systems: https://docs.python.org/3/using/index.html.

=================
Installing Pip
=================

The official guide to installing Pip can be found here: https://pip.pypa.io/en/stable/installation/.

Pip is a python package manager which you can use to install python libraries or applications.

First, you may already have pip installed, especially if you've just downloaded and installed Python. You can check by running the following command in a shell::

    pip --version


If you do not have it installed, you can install it by running the following commands

For Max or Linux::
    python -m ensurepip --upgrade

For Windows::
    py -m ensurepip --upgrade


====================
Installing an IDE
====================

You can, of course, write your code in any text editor you want, then save it with a `.py` extension and run it from a shell like so

For Mac or Linux::
    python example.py

For Windows::
    py example.py


But certain text editors provide a bit more functionality for writing code, such as syntax highlighting, auto-formatting and a shell within the same window.
A very popular such editor (also called an IDE) is Visual Studio Code. Although this is a Microsoft product, there are free versions of it available for most 
operating systems, so you do not need to own a Windows machine to be able to install and use it. You can download an installer from https://code.visualstudio.com/.

===================================
Installing Turtle Oxford for Python
===================================

The code for Turtle Oxford is hosted entirely on GitHub at the following address: https://github.com/turtleoxford/turtle-python.

You can install the package in a shell, using pip with the following command::
    pip install git+https://github.com/turtleoxford/turtle-python.git


=============================
Executing one of the examples
=============================

You can execute one of the Oxford Turtle Python examples from https://github.com/turtleoxford/turtle-python/tree/main/examples by downloading them
and then running the following command in a shell (`draw_pause.py` is just one of the file names, it could be any of them):

On Mac or Linux::
    python draw_pause.py

Or on Windows::
    py draw_pause.py


==========================
Writing your own programme
==========================

The structure of one of Oxford Turtle Python programmes is as follows::

    from turtle_oxford import *  # This tells the interpreter to import all symbols from the Turtle module
    from math import *           # Optional: import one or more other packages and their symbols, math is a useful one\

    with turtle_canvas(0, 0, 500, 500) as t: # Create the canvas with the desired dimensions, you can omit the parameters to use the default size
        <Turtle Commands>


You can execute this like any other python file, like in the previous section.