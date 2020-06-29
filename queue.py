"""
Last modified: 29.06.2020

The queue class is defined here. It is the stick with which you play the game.
"""

from graphics import *
from table import *
from ball import *


class Queue:
    def __init__(self, _v, _a, _texture):
        self.v = _v
        self.a = _a
        self.texture = _texture

        self.x = 0.0
        self.y = 0.0
        v_reset = _v
        self.visible = False
        self.move = False
        xZiel = 0.0
        xZielMax = 150.0

        x_shadow = 40
        y_shadow = -30

        self.design = 1

        mouse_x = 0  # self?
        mouse_y = 0  # self?
        zielhilfeZeichnen = True

    def init_position(self, whiteBall, zoom):
        if self.visible == False:
            self.x = whiteBall.x + whiteBall.radius * zoom
            self.y = whiteBall.y
            self.visible = True

    def init_postion2(self, whiteBall, zoom):
        self.x = whiteBall.x + whiteBall.radius * zoom
        self.y = whiteBall.y
        self.visible = True

    def set_mouse(self, _mouse_x, _mouse_y):
        """....

        Args:
            _mouse_x (int): x coordinate of the mouse position
            _mouse_y (int): y coordinate of the mouse position
        """
        if self.move == False and self.xZiel == 0.0:
            self.mouse_x = _mouse_x
            self.mouse_y = _mouse_y

    def draw(self, whiteBall, table, zoom):
        """Draw the queue. There are three designs...

        Args:
            whiteBall (object): [description]
            table (object): [description]
            zoom (float): [description]
        """
        if self.visible == True:
            cos_alpha = (self.mouse_x - whiteBall.x) / np.sqrt((self.mouse_x - whiteBall.x) ** 2 + (self.mouse_y - whiteBall.y) ** 2)
            alpha = np.arccos(cos_alpha)

            if whiteBall.y > self.mouse_y:
                alpha = -alpha

            glPushMatrix()
            glTranslatef(whiteBall.x, whiteBall.y, 0.0)
            glScalef(1.0 / zoom, 1.0 / zoom, 1.0 / zoom)
            glRotatef(alpha * 180.0 / np.pi, 0.0, 0.0, 1.0)
            glTranslatef(-whiteBall.x, -whiteBall.y, 0.0)

            # Design option 1
            if self.design == 1:
                glBegin(GL_QUADS)

                glColor3f(0.1, 0.1, 0.1)
                glVertex2f(self.x, self.y + 2)
                glVertex2f(self.x + 2, self.y + 2)
                glVertex2f(self.x + 2, self.y - 2)
                glVertex2f(self.x, self.y - 2)

                glColor3f(0.8, 0.8, 0.8)
                glVertex2f(self.x + 2, self.y + 2)
                glVertex2f(self.x + 2, self.y - 2)
                glVertex2f(self.x + 15, self.y - 3)
                glVertex2f(self.x + 15, self.y + 3)

                glColor3f(0.6, 0.5, 0.2)
                glVertex2f(self.x + 15, self.y + 3)
                glVertex2f(self.x + 15, self.y - 3)
                glVertex2f(self.x + 200, self.y - 5)
                glVertex2f(self.x + 200, self.y + 5)

                glColor3f(0.0, 0.0, 0.0)
                glVertex2f(self.x + 80, self.y)
                glVertex2f(self.x + 80, self.y)
                glVertex2f(self.x + 200, self.y - 5)
                glVertex2f(self.x + 200, self.y + 5)

                glVertex2f(self.x + 200, self.y - 5)
                glVertex2f(self.x + 200, self.y + 5)
                glVertex2f(self.x + 400, self.y + 6)
                glVertex2f(self.x + 400, self.y - 6)

                glEnd()

            if self.design == 2:
                queue_top = 5
                queue_length = 400
                queue_end = 10

                glBegin(GL_QUADS)
                glColor3f(1.0, 0.0, 1.0)
                glVertex2f(self.x, self.y - queue_top / 2)
                glVertex2f(self.x, self.y + queue_top / 2)
                glColor3f(1.0, 1.0, 0.0)
                glVertex2f(self.x + queue_length, self.y + queue_end / 2)
                glVertex2f(self.x + queue_length, self.y - queue_end / 2)
                glEnd()

                glBegin(GL_QUADS)
                glColor3f(0.0, 0.0, 0.0)
                glVertex2f(self.x, self.y - queue_top / 2)
                glVertex2f(self.x, self.y + queue_top / 2)
                glVertex2f(self.x + 2, self.y + queue_top / 2)
                glVertex2f(self.x + 2, self.y - queue_top / 2)
                glEnd()

            if self.design == 3:
                queue_top = 20
                queue_length = 100
                queue_end = 20

                # yellow rectangle
                glBegin(GL_QUADS)
                glColor3f(1.0, 1.0, 0.0)
                glVertex2f(self.x + 30, self.y - queue_top / 2)
                glVertex2f(self.x + 30, self.y + queue_top / 2)
                glColor3f(1.0, 1.0, 0.0)
                glVertex2f(self.x + queue_length, self.y + queue_end / 2)
                glVertex2f(self.x + queue_length, self.y - queue_end / 2)

                # black stripe
                glBegin(GL_QUADS)
                glColor3f(0.0, 0.0, 0.0)
                glVertex2f(self.x + 30, self.y - queue_top / 4)
                glVertex2f(self.x + 30, self.y + queue_top / 4)
                glVertex2f(self.x + queue_length, self.y + queue_end / 4)
                glVertex2f(self.x + queue_length, self.y - queue_end / 4)

                # red end
                glBegin(GL_QUADS)
                glColor3f(1.0, 0.0, 0.0)
                glVertex2f(self.x + queue_length, self.y - queue_top / 1.9)
                glVertex2f(self.x + queue_length, self.y + queue_top / 1.9)
                glVertex2f(self.x + queue_length + 5.5, self.y + queue_end / 2.8)
                glVertex2f(self.x + queue_length + 5.5, self.y - queue_end / 2.8)

                # brown top
                glBegin(GL_QUADS)
                glColor3f(0.8, 0.6, 0.3)
                glVertex2f(self.x, self.y)
                glVertex2f(self.x, self.y)
                glVertex2f(self.x + 30, self.y + queue_top / 2)
                glVertex2f(self.x + 30, self.y - queue_top / 2)

                # gray top
                glBegin(GL_QUADS)
                glColor3f(0.3, 0.3, 0.3)
                glVertex2f(self.x, self.y)
                glVertex2f(self.x, self.y)
                glVertex2f(self.x + 10, self.y + queue_top / 4.5)
                glVertex2f(self.x + 10, self.y - queue_top / 4.5)

                # small brown triangle 1
                glBegin(GL_QUADS)
                glColor3f(0.8, 0.6, 0.3)
                glVertex2f(self.x + 30, self.y + queue_top / 2)
                glVertex2f(self.x + 30, self.y)
                glVertex2f(self.x + 35, self.y + queue_top / 4)
                glVertex2f(self.x + 35, self.y + queue_top / 4)

                # small brown triangle 2
                glBegin(GL_QUADS)
                glColor3f(0.8, 0.6, 0.3)
                glVertex2f(self.x + 30, self.y - queue_top / 2)
                glVertex2f(self.x + 30, self.y)
                glVertex2f(self.x + 35, self.y - queue_top / 4)
                glVertex2f(self.x + 35, self.y - queue_top / 4)

                glEnd()

            glPopMatrix()

            # draw target assistance
            if (self.visible == True) and (zielhilfeZeichnen == True):

                if (self.move == 0) and (xZiel == 0):
                    cos_alpha = (self.mouse_x - whiteBall.x) / np.sqrt((self.mouse_x - whiteBall.x) ** 2 + (self.mouse_y - whiteBall.y) ** 2)
                    alpha = np.arccos(cos_alpha)

                    if whiteBall.y > self.mouse_y:
                        alpha = -alpha

                    spielfeldbreite = tisch.get_spielfeldbreite()
                    spielfeldhoehe = tisch.get_spielfeldhoehe()
                    bande = tisch.get_bande()

                    yZielhilfe = spielfeldhoehe
                    xZielhilfe = (x * yZielhilfe) / y

                    d = np.sqrt(yZielhilfe ** 2 + xZielhilfe ** 2)

                    length = 3000

                    x1 = whiteBall.x  # - whiteBall.radius
                    y1 = whiteBall.y
                    x2 = self.x - whiteBall.radius - np.cos(alpha) * length
                    y2 = self.y + np.sin(-alpha) * length
                    x3 = x2
                    y3 = y2

                    if y2 > spielfeldhoehe - bande:
                        m = (y2 - y1) / (x2 - x1)
                        delta_x = (spielfeldhoehe - bande - y1) / m

                        x2 = x1 + delta_x
                        y2 = spielfeldhoehe - bande

                        if delta_x > 0:
                            x3 = x2 + length
                            y3 = y2 - m * length
                        else:
                            x3 = x2 - length
                            y3 = y2 + m * length

                    if y2 < bande:
                        m = (y2 - y1) / (x2 - x1)
                        delta_x = (bande - y1) / m

                        x2 = x1 + delta_x
                        y2 = bande

                        if delta_x < 0:
                            x3 = x2 - length
                            y3 = y2 + m * length
                        else:
                            x3 = x2 + length
                            y3 = y2 - m * length

                    if x2 > spielfeldbreite - bande:
                        m = (x2 - x1) / (y2 - y1)
                        delta_y = (spielfeldbreite - bande - x1) / m

                        x2 = spielfeldbreite - bande
                        y2 = y + delta_y

                        if delta_y < 0:
                            x3 = x2 + m * length
                            y3 = y2 - length
                        else:
                            x3 = x2 - m * length
                            y3 = y2 + length

                    if x2 < bande:
                        m = (x2 - x1) / (y2 - y1)
                        delta_y = (bande - x1) / m

                        x2 = bande
                        y2 = y1 + delta_y

                        if delta_y < 0:
                            x3 = x2 + m * length
                            y3 = y2 - length
                        else:
                            x3 = x2 - m * length
                            y3 = y2 + length

                    if y3 > spielfeldhoehe - bande:
                        m = (y3 - y2) / (x3 - x2)
                        delta_x = (spielfeldhoehe - bande - y2) / m

                        x3 = x2 + delta_x
                        y3 = spielfeldhoehe - bande

                    if y3 < bande:
                        m = (y3 - y2) / (x3 - x2)
                        delta_x = (bande - y2) / m

                        x3 = x2 + delta_x
                        y3 = bande

                    if x3 > spielfeldbreite - bande:
                        m = (x3 - x2) / (y3 - y2)
                        delta_y = (spielfeldbreite - bande - x2) / m

                        x3 = spielfeldbreite - bande
                        y3 = y2 + delta_y

                    if x3 < bande:
                        m = (x3 - x2) / (y3 - y2)
                        delta_y = (bande - x2) / m

                        x3 = bande
                        y3 = y2 + delta_y

                    glLineWidth(3.5)
                    glEnable(GL_BLEND)
                    glBlendFunc(GL_ONE, GL_ONE)

                    glBegin(GL_LINE_STRIP)

                    glColor3f(0.2, 0.2, 0.2)
                    glVertex2f(x1, y1)
                    glVertex2f(x2, y2)
                    glVertex2f(x3, y3)

                    glEnd()
                    glLineWidth(1.0)
                    glDisable(GL_BLEND)


"""missing !!!"""
