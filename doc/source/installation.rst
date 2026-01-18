Installation
============

Installing Python
-----------------

If you don't have Python installed, download it from the official website:

1. Visit https://www.python.org/downloads/
2. Download the latest version of Python (3.10 or higher)
3. Run the installer
4. **Important:** On Windows, check the box "Add Python to PATH" during installation
5. Verify installation by opening a terminal/command prompt and typing:

   .. code-block:: bash

      python --version

Requirements
------------

* Python 3.10 or higher
* tkinter (usually included with Python)
* Pillow

Python Package Managers
-----------------------

Python uses package managers to install libraries and dependencies. This project supports two options:

**pip** (Python's default package manager)

pip comes pre-installed with Python. It's the standard tool for installing Python packages. Most beginners should use pip.

.. code-block:: bash

   # Check if pip is installed
   pip --version

**uv** (Modern, faster alternative)

uv is a newer, faster package manager for Python. It's optional but recommended for advanced users.

.. code-block:: bash

   # Install uv (optional)
   pip install uv
   
   # Check if uv is installed
   uv --version

Installation from Source
-------------------------

Clone the repository and install in editable mode:

**Using pip:**

.. code-block:: bash

   git clone https://github.com/turtleoxford/turtle-python.git
   cd turtle-python
   pip install -e .

**Using uv:**

.. code-block:: bash

   git clone https://github.com/turtleoxford/turtle-python.git
   cd turtle-python
   uv pip install -e .