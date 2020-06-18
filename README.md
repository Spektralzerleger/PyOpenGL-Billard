# PyOpenGL-Billard
This will be a Billard game implemented in Python using the PyOpenGL Library.

## Installation
In order to run the program, you need to install PyOpenGL. This can be done via pip:
```
pip install PyOpenGL PyOpenGL_accelerate
```
However, for Windows user (like me) I recommend to download the necessary packages from this 
[website](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl)
and install them manually. E.g. for Python 3.6 and a 64 bit architecture download the files

_PyOpenGL-3.1.5-cp36-cp36-win_amd64.whl_ and <br/>
_PyOpenGL_accelerate-3.1.5-cp36-cp36-win_amd64.whl_

Open the Command Prompt (cmd.exe) as administrator. Change to the download directory and install the packages by
```
pip install PyOpenGL-3.1.5-cp36-cp36-win_amd64.whl
pip install PyOpenGL_accelerate-3.1.5-cp36-cp36-win_amd64.whl
```
If the package is already installed, but doesn't work, then you have to ignore the currently installed package:
```
pip install --ignore-installed PyOpenGL-3.1.5-cp36-cp36-win_amd64.whl
pip install --ignore-installed PyOpenGL_accelerate-3.1.5-cp36-cp36-win_amd64.whl
```
You can check whether your installation was successful. Try to import the OpenGL library in your python script:
```python
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print("ERROR: PyOpenGL not installed properly.")
```
