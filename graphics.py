'''
Last modified: 16.06.2020
Graphics help functions, which enable a comfortable usage of the OpenGL libraries.
'''

import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

graphicsTextBlending = False
sphere = GLUquadricObj()

# prevents that changing the window size changes the displayed graphics
def graphicsChangeSize(width, height):
    return

# initialize a GLUT-graphics window
def graphicsInit(windowname, width, height, zoom):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(int(zoom * width), int(zoom * height))
    glutInitWindowPosition(0, 20)
    glutCreateWindow(windowname)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    # glutReshapeFunc(graphicsChangeSize)
    glEnable(GL_TEXTURE_2D)


# draw ball with center (x, y) and radius
# color can be set right infront of the function
def graphicsBall(x, y, radius):
    glBegin(GL_POLYGON)
    step = np.pi / 32
    for angle in np.arange(0.0, 2*np.pi, step):
        glVertex2f(x + radius*np.cos(angle), y + radius*np.sin(angle))
    glVertex2f(x + radius, y)
    glEnd()


'''
# displays text as Bitmap
# takes position (x, y) and text as string
def graphicsText(x, y, text):
    if graphicsTextBlending:
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE)

    glRasterPos2f(x, y)
    
    for(int i = 0; i < strlen(text); i++)
    glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_10, text[i])
    
    if graphicsTextBlending:
        glDisable(GL_BLEND)
'''


def graphicsInit3D(width, height):
    # create sphere
    sphere = gluNewQuadric()
    gluQuadricNormals(sphere, GLU_SMOOTH)
    gluQuadricTexture(sphere, GL_TRUE)

    # create and turn on light
    light_ambient = [0.33, 0.33, 0.33, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)


def graphicsEnable3D(width, height):
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
    gluSphere(sphere, radius, 20, 20)