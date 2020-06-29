"""
Last modified: 29.06.2020

Graphics help functions, which enable a comfortable usage of the OpenGL libraries.
"""

import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *



def graphicsChangeSize(width, height):
    """Prevents that changing the window size changes the displayed graphics.

    Args:
        width (int): Window width
        height (int): Window height
    """
    return


def graphicsInit(windowname, width, height, zoom):
    """Initialize a GLUT-graphics window.

    Args:
        windowname (str): Name of the GLUT window, e.g. "Billard".
        width (int): Window width
        height (int): Window height
        zoom (float): Zoom factor to scale the window size
    """
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(int(zoom * width), int(zoom * height))
    glutInitWindowPosition(0, 20)
    glutCreateWindow(windowname)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    # glutReshapeFunc(graphicsChangeSize)


def graphicsBall(x, y, radius):
    """Draw 2D ball with center (x, y) and radius. Color can be set right in front of the function.

    Args:
        x (int): x coordinate of ball center
        y (int): y coordinate of ball center
        radius (float): Radius of the ball
    """
    glBegin(GL_POLYGON)
    step = np.pi / 32
    for angle in np.arange(0.0, 2 * np.pi, step):
        glVertex2f(x + radius * np.cos(angle), y + radius * np.sin(angle))
    glVertex2f(x + radius, y)
    glEnd()


def graphicsText(x, y, text):
    """Displays text as Bitmap.

    Args:
        x (int): x coordinate of position.
        y (int): y coordinate of position.
        text (str): Text you want to display.
    """
    glRasterPos2f(x, y)
    for i in range(len(text)):
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_10, ord(text[i]))


def graphicsInit3D(width, height):
    """Initialize 3D graphics mode.

    Args:
        width (int): what width?
        height (int): what height?
    """
    global sphere
    # Create sphere
    sphere = gluNewQuadric()
    gluQuadricNormals(sphere, GLU_SMOOTH)
    gluQuadricTexture(sphere, GL_TRUE)

    # Create and turn on light
    light_ambient = [0.33, 0.33, 0.33, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)


def graphicsEnable3D(width, height):
    """Enable 3D graphics mode.

    Args:
        width (int): what width?
        height (int): what height?
    """
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(0.0, width, 0.0, height, -100.0, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glColor3f(1.0, 1.0, 1.0)


def graphicsDisable3D(width, height, zoom):
    """Disable 3D graphics mode.

    Args:
        width (int): ?
        height (int): ?
        zoom (float): Zoom factor to scale the window size
    """
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)
    glDisable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glScalef(zoom, zoom, zoom)


def graphicsBall3D(radius):
    """Draw 3D ball with given radius.

    Args:
        radius (float): Radius of the ball
    """
    gluSphere(sphere, radius, 20, 20)
