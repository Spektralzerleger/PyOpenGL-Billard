"""
Edited by: Eugen Dizer
Last modified: 28.06.2020

This is the main part of the code where the GLUT window is initialized and the graphics is rendered.
Here, you can also change the setup like the number of balls, their friction or the window size.

"""

from graphics import *
from mytime import *
from table import *
from ball import *
# from queue import *
from textures import *


"""
Rewrite this C++ Code into Python!!!

UNITS: 1 corresponds to 1mm in reality
"""


# Gameboard size
border = 100
width = 2540 + 2 * border
height = 1270 + 2 * border

# Window size
zoom = 0.4
window_width = int((width + 275) * zoom)
window_height = int((height + 150) * zoom)

# Hole and ball size
holesize_middle = 62
holesize_edges = 65
ballRadius = 29.1


gameover = False

# Number of balls
N = 16

# Time measurement
t = 0.0
takt = 0.0004


def display():
    global gameover
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    table.draw()

    """
    queue.balkenzeichnen(tisch)
    """
    for i in range(N):
        ball[i].draw_shadow()

    """
    queue.schatten_zeichnen(kugel[0], zoom)
    """
    graphicsEnable3D(window_width, window_height)
    for i in range(N):
        ball[i].draw3d(zoom)
    graphicsDisable3D(window_width, window_height, zoom)

    """
    queue.zeichnen(kugel[0], tisch, zoom)
    """

    if ball[8].visible == False:
        gameover = True
        table.drawGameover()

    glFlush()
    glutSwapBuffers()


def idle():
    global t
    # timeflow
    t = t + diff_seconds()

    """
    Fix idle and collision function!!!
    """

    if t > 0.25:
        t = 0.0

    while t > takt and gameover == False:
        stand = 0

        for i in range(N):
            if ball[i].move(takt) == False:
                stand += 1

        if stand == N:
            if ball[0].visible == False:
                ball[0].x = 600
                ball[0].y = height / 2
                ball[0].visible = True
                ball[0].potted = False
                ball[0].radius = ballRadius
                ball[0].shift = True
        """
            if ball[0].potted == False:
                queue.init_position(ball[0], zoom)
        """
        for i in range(N):
            ball[i].collision(table, takt)
            # ball[i].ausrollen(takt)
        """
        for i in range(N):
            for j in range(i+1, N):
                ball[i].stossen(balls[j], takt)

        queue.anstossen(kugel[0], takt)
        """
        t -= takt

    display()  # or glutPostRedisplay()


"""
# is called when a button is pressed
def keyboard(key, x, y):
  
  if (key == 'm'):
     for i in range(N):
       if (kugel[i].potted == False):
         ball[i].vx = 0.0
         ball[i].vy = 0.0
  
  if(key == 'n') {
    initBalls();
    queue.init_postion2(kugel[0], zoom);
  }
  
  if(key == 'q')     
    exit(0);
    
  if(key == '1')
    queue.set_design(1);
    
  if(key == '2')
    queue.set_design(2);
    
  if(key == '3')
    queue.set_design(3);
    
  if(key == 'z') 
    queue.toggle_zielhilfe();   
    
    
  if(key == 'w'){
           
    if(kugel[0].get_verschieben()){
      if(kugel[0].get_y() + kugel[0].get_radius() <  hoehe - bande - 7.5) {                            
        kugel[0].set_y ( kugel[0].get_y() + 10 / zoom);
        queue.init_postion2(kugel[0], zoom);
        }
      }
  }
  
  if(key == 's'){
      if(kugel[0].get_verschieben()){
          if(kugel[0].get_y() + kugel[0].get_radius() >  kugel[0].get_radius() + bande +37.5 ) {                      
            kugel[0].set_y ( kugel[0].get_y() - 10 / zoom);
            queue.init_postion2(kugel[0], zoom); 
          }
      }
  }
       
}
  
# is called when a mouse button is pressed
def mouse(button, state, x, y):   
    if state == GLUT_DOWN:
        ball[0].shift = False
        queue.set_bewegung(true);

    if state == GLUT_UP:
        queue.set_bewegung(false);  


# is called when you move the mouse
def mouseMotion(x, y):
    queue.set_mouse(int(x / zoom), int((fensterHoehe - y) / zoom));


# call this funtion when size of the window changes
def reshape(width, height):
    glutReshapeWindow(window_width, window_height)
"""


def initTable():
    """Here we initialize our billard table. The table has the following properties:
            Table(width, height, border, holesize_middle, holesize_edges, table_texture, balken_texture, gameover_texture)
        * width, height = width and height of the whole table
        * border = size of the brown border
        * holesize_middle = size of the holes in the upper and lower middle
        * holesize_edges = size of the holes on the edges
        * table_texture = texture of the table
        * balken_texture = texture of the wood above the table
        * gameover_texture = texture for "game over" scene in the end
    """
    global table
    # Load textures
    table_texture = load_texture("Textures/tisch.bmp")
    balken_texture = load_texture("Textures/balken.bmp")
    gameover_texture = load_texture("Textures/gameover.bmp")

    table = Table(width, height, border, holesize_middle, holesize_edges, table_texture, balken_texture, gameover_texture)


def initBalls():
    """Here we initialize our 16 balls. A ball has the following properties:
            Ball(x, y, radius, vx, vy, r, g, b, m, number)
        * x, y = Initial (x, y) position coordinates
        * radius = Ball radius
        * vx, vy = Initial (x, y) velocity components
        * r, g, b = ???
        * m = Mass of the ball (do I need it?)
        * number = Ball number, defines also texture (e.g. 8 = black 8)
    """
    global ball
    # List of all balls, sorted by their number
    ball = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    ball[0] = Ball(600, height / 2, ballRadius, 0.0, 0.0, 1.0, 1.0, 1.0, 10, 0)
    ball[1] = Ball(1815, height / 2, ballRadius, -400.0, 600.0, 1.0, 0.8, 0.0, 10, 1)
    ball[2] = Ball(1870 + 55, height / 2 + 70, ballRadius, -0.0, 0.0, 0.0, 0.0, 0.67, 10, 2)
    ball[3] = Ball(1870 + 55, height / 2 - 70, ballRadius, -0.0, 0.0, 1.0, 0.0, 0.0, 10, 3)
    ball[4] = Ball(1870 + 3 * 55, height / 2 + 70, ballRadius, -0.0, 0.0, 0.4, 0.0, 0.6, 10, 4)
    ball[5] = Ball(1870 + 3 * 55, height / 2 + 2 * 70, ballRadius, -0.0, 0.0, 1.0, 0.5, 0.0, 10, 5)
    ball[6] = Ball(1870 + 3 * 55, height / 2 - 70, ballRadius, -0.0, 0.0, 0.2, 0.7, 0.2, 10, 6)
    ball[7] = Ball(1870 + 2 * 55, height / 2 + 35, ballRadius, -0.0, 0.0, 0.5, 0.0, 0.0, 10, 7)
    ball[8] = Ball(1870 + 55, height / 2, ballRadius, -0.0, 0.0, 0.0, 0.0, 0.0, 10, 8)
    ball[9] = Ball(1870 + 3 * 55, height / 2, ballRadius, -0.0, 0.0, 1.0, 0.8, 0.0, 10, 9)
    ball[10] = Ball(1870 + 3 * 55, height / 2 - 2 * 70, ballRadius, -0.0, 0.0, 0.0, 0.0, 0.67, 10, 10)
    ball[11] = Ball(1870 + 2 * 55, height / 2 + 35 + 70, ballRadius, -0.0, 0.0, 1.0, 0.0, 0.0, 10, 11)
    ball[12] = Ball(1870 + 2 * 55, height / 2 - 35, ballRadius, -0.0, 0.0, 0.4, 0.0, 0.6, 10, 12)
    ball[13] = Ball(1870 + 2 * 55, height / 2 - 35 - 70, ballRadius, -0.0, 0.0, 1.0, 0.5, 0.0, 10, 13)
    ball[14] = Ball(1870, height / 2 + 35, ballRadius, -0.0, 0.0, 0.2, 0.7, 0.2, 10, 14)
    ball[15] = Ball(1870, height / 2 - 35, ballRadius, -0.0, 0.0, 0.5, 0.0, 0.0, 10, 15)


def main():
    # Initialize graphics:
    graphicsInit("Billard", width + 275, height + 150, zoom)
    graphicsInit3D(width, height)

    # Initialize objects
    initTable()
    # queue = Queue()
    initBalls()

    # Register display function:
    glutDisplayFunc(display)

    # Register idle function:
    glutIdleFunc(idle)

    """
    # register keyboard function:
    glutKeyboardFunc(keyboard)

    # register mouse function
    glutMouseFunc(mouse)
    glutPassiveMotionFunc(mouseMotion)

    # glutReshapeFunc(reshape)
    
    textureBalken = LadeTextur("Texturen/balken.bmp")
    tisch.init(breite, hoehe, bande, 0.5, 0.0, 0.0, 0.0, 0.5, 0.0, lochgroesseMitte, lochgroesseEcke, 0.0, 0.0, 0.0, LadeTextur("Texturen/tisch.bmp"), texturBalken, LadeTextur("Texturen/gameover.bmp"));    

    initKugeln()

    queue.init(100.0, 15000.0, texturBalken)
    queue.init_position(kugel[0], zoom)

    # time measurement:
    diff_seconds()       # do I need this?
    """

    # Show window:
    glutMainLoop()


if __name__ == "__main__":
    main()
