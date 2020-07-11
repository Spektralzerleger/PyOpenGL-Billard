"""
Edited by: Eugen Dizer
Last modified: 11.07.2020

This is the main part of the code where the GLUT window is initialized and the graphics is rendered.
Here, you can also change the setup like the number of balls, their friction or the window size.

To do: FIX bugs!!!
Bugs: Idle function too slow! (Maybe with Timer or pygame window?)
Maybe improve texture loading, rendering, mipmaps, frame buffer objects...

UNITS: 1 corresponds to 1mm in reality
"""

from graphics import *
from mytime import *
from table import *
from ball import *
from queue import *
from textures import *


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

# Number of balls
N = 16

gameover = False


def display():
    """This function says what is drawn and shown on the display.
    """
    global gameover
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    table.draw()

    # Draw the strength indicator bar
    queue.draw_bar(table)

    for i in range(N):
        ball[i].draw_shadow()

    queue.draw_shadow(ball[0], zoom)

    graphicsEnable3D(window_width, window_height)
    for i in range(N):
        ball[i].draw3d(zoom)
    graphicsDisable3D(window_width, window_height, zoom)

    queue.draw(ball[0], table, zoom)

    if ball[8].visible == False:
        gameover = True
        table.drawGameover()

    glFlush()
    glutSwapBuffers()
    return


def idle():
    """This function is responsible for the continuous animation.
    The idle callback is continuously called when events are not being received.
    """
    # How much time has passed since the last frame
    dt = diff_seconds()

    """
    Fix idle and collision function!!
    """
    # One needs smaller time steps to capture the collisions accurately.
    # Larger time steps will lead to a strange collision behavior.
    stand = 0

    # Check for standing balls
    for i in range(N):
        if ball[i].move(dt) == False:
            stand += 1

    if stand == N:
        if ball[0].visible == False:
            ball[0].x = 600
            ball[0].y = height / 2
            ball[0].vx = 0.0
            ball[0].visible = True
            ball[0].potted = False
            ball[0].radius = ballRadius
            ball[0].shift = True

        if ball[0].potted == False:
            queue.init_position(ball[0], zoom)

    # Check the collision with the table
    for i in range(N):
        ball[i].table_collision(table, dt)
        ball[i].roll_out(dt)

    # Check the collision with other balls
    for i in range(N):
        for j in range(i + 1, N):
            ball[i].ball_collision(ball[j], dt)

    # Move the queue
    queue.hit(ball[0], dt)

    # Redraw the scene
    glutPostRedisplay()
    return


def keyboard(key, x, y):
    """This function is called when a button is pressed.
    Maybe make a menu where you can see all the possible keys and their actions.

    Args:
        key (bytes): Generated character which key is pressed.
        x (int): x coordinate (window relative) of the mouse when the key was pressed.
        y (int): y coordinate (window relative) of the mouse when the key was pressed.
    """
    # Convert bytes object to string
    key = key.decode("utf-8")

    if key == "m":
        for i in range(N):
            if ball[i].potted == False:
                ball[i].vx = 0.0
                ball[i].vy = 0.0

    if key == "n":
        initBalls()
        queue.init_postion2(ball[0], zoom)

    if key == "q":
        sys.exit()

    if key == "1":
        queue.design = 1

    if key == "2":
        queue.design = 2

    if key == "3":
        queue.design = 3

    if key == "z":
        queue.draw_target_assistance = not queue.draw_target_assistance

    if key == "w":
        if ball[0].shift == True:
            if ball[0].y + ball[0].radius < height - border - 7.5:
                ball[0].y = ball[0].y + 10 / zoom
                queue.init_postion2(ball[0], zoom)

    if key == "s":
        if ball[0].shift == True:
            if ball[0].y + ball[0].radius > ball[0].radius + border + 37.5:
                ball[0].y = ball[0].y - 10 / zoom
                queue.init_postion2(ball[0], zoom)
    return


def mouse(button, state, x, y):
    """This function is called when a mouse button is pressed.

    Args:
        button (int): Which mouse button is pressed (GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, or GLUT_RIGHT_BUTTON).
        state (int): Is the mouse pressed or released? (GLUT_DOWN or GLUT_UP)
        x (int): x coordinate (window relative) of the mouse when the button was pressed.
        y (int): y coordinate (window relative) of the mouse when the button was pressed.
    """
    if state == GLUT_DOWN:
        ball[0].shift = False
        queue.move = True

    if state == GLUT_UP:
        queue.move = False
    return


def mouseMotion(x, y):
    """This function is called when you move the mouse.

    Args:
        x (int): x coordinate (window relative) of the mouse.
        y (int): y coordinate (window relative) of the mouse.
    """
    queue.mouse_x = int(x / zoom)
    queue.mouse_y = int((window_height - y) / zoom)
    return


def reshape(width, height):
    """This function is called when you try to reshape your window.

    Args:
        width (int): Window width.
        height (int): Window height.
    """
    glutReshapeWindow(window_width, window_height)
    return


def initTable():
    """Here we initialize our billard table. The table has the following properties:
            Table(width, height, border, holesize_middle, holesize_edges, table_texture, balken_texture, gameover_texture)
        * width, height = Width and height of the whole table.
        * border = Size of the brown border.
        * holesize_middle = Size of the holes in the upper and lower middle.
        * holesize_edges = Size of the holes on the edges.
        * table_texture = Texture of the table.
        * balken_texture = Texture of the wood above the table.
        * gameover_texture = Texture for "game over" scene in the end.
    """
    global table
    # Load textures
    table_texture = load_texture("Textures/tisch.bmp")
    balken_texture = load_texture("Textures/balken.bmp")
    gameover_texture = load_texture("Textures/gameover.bmp")

    table = Table(width, height, border, holesize_middle, holesize_edges, table_texture, balken_texture, gameover_texture)
    return


def initBalls():
    """Here we initialize our 16 balls. A ball has the following properties:
            Ball(x, y, radius, vx, vy, r, g, b, m, number)
        * x, y = Initial (x, y) position coordinates.
        * radius = Ball radius.
        * vx, vy = Initial (x, y) velocity components.
        * r, g, b = RGB color values for the case that no texture is available.
        * m = Mass of the ball (do I need it?) -> maybe define on the top of main.py
        * number = Ball number, defines also texture (e.g. 8 = black 8).
    """
    global ball
    # List of all balls, sorted by their number
    ball = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    ball[0] = Ball(600, height / 2, ballRadius, 0.0, 0.0, 1.0, 1.0, 1.0, 10, 0)
    ball[1] = Ball(1815, height / 2, ballRadius, 0.0, 0.0, 1.0, 0.8, 0.0, 10, 1)
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
    return


def initQueue():
    """Here we initialize the queue. The queue has the following properties:
            Queue(v, a, texture)
        * v = Initial velocity. How fast it should move backwards.
        * a = Initial acceleration. How fast it should accelerate towards the white ball.
        * texture = Texture of the strength indicator on the right side of the window.
    """
    global queue, ball
    # Load texture (think about a more efficient way?)
    balken_texture = load_texture("Textures/balken.bmp")

    queue = Queue(80.0, 2000.0, balken_texture)
    return


def main():
    # Initialize window graphics:
    graphicsInit("Billard", width + 275, height + 150, zoom)
    graphicsInit3D()

    # Initialize objects:
    initTable()
    initBalls()
    initQueue()
    queue.init_position(ball[0], zoom)

    # Register display function:
    glutDisplayFunc(display)

    # Register idle function:
    glutIdleFunc(idle)

    # Register keyboard function:
    glutKeyboardFunc(keyboard)

    # Register mouse functions:
    glutMouseFunc(mouse)
    glutPassiveMotionFunc(mouseMotion)

    # Register reshape function:
    glutReshapeFunc(reshape)

    # Show window:
    glutMainLoop()


if __name__ == "__main__":
    main()
