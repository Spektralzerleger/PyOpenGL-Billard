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
If you still encounter problems when compiling, try to upgrade your numpy version or uninstall PyOpenGL_accelerate. <br/>
Moreover, I use PIL to load the textures and work with the images. If you haven't installed it, try
```
pip install Pillow
```
## The Game
Short story: Originally, the game was implemented in C++ when I participated at the JuniorScienceAcademy in 2013. <br/>
Now, I wanted to refresh my knowledge in OpenGL and "translate" the code to Python.

The actual game looks something like this:
<p align="center">
  <img src="https://user-images.githubusercontent.com/37344742/86500252-201e0500-bd90-11ea-81be-1249bde20171.png">
</p>

### Features: <br/>
* Three different design options for the queue
* Possibility to turn on a target assistance (white ray)
* Strength visualization with a colorbar on the right
* Score visualization of the potted balls of each player
* Possibility to adjust the mass, size, friction etc. of the balls
* Possibility to stop the motion or restart the game

### Bugs: <br/>
This code runs very slow with Python! One could do only one calculation step in the idle function but then the physics would break and it would come to unrealistic collision effects. So, one has to improve the computation time and speed up the rendering process.
