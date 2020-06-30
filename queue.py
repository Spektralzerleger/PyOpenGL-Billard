"""
Last modified: 30.06.2020

The queue class is defined here. It is the stick with which you play the game.
The top of the queue is positioned right on the balls surface and moves when you
move your mouse. When you click, it loads and moves backwards. When you release,
it hits the ball and gives it an initial speed. While the balls are moving, the
queue is not visible. You have three different design options.

FIX bug: Queue and White ball move after it was potted and reappears...
"""

from graphics import *
from table import *
from ball import *


class Queue:
    def __init__(self, _v, _a, _texture):
        """Initialize the queue.

        Args:
            _v (float): Initial speed
            _a (float): Initial acceleration
            _texture (int): Texture ID number
        """
        self.v = _v
        self.a = _a
        self.texture = _texture

        # Comment (private variables)
        self.x = 0.0
        self.y = 0.0
        self.v_reset = _v
        self.visible = False
        self.move = False
        self.xTarget = 0.0
        self.xTargetMax = 150.0

        self.x_shadow = 40
        self.y_shadow = -30

        self.design = 1

        self.mouse_x = 0
        self.mouse_y = 0

        self.draw_target_assistance = True

    def init_position(self, whiteBall, zoom):  # decide which one to take...
        if self.visible == False:
            self.x = whiteBall.x + whiteBall.radius * zoom
            self.y = whiteBall.y
            self.visible = True

    def init_postion2(self, whiteBall, zoom):
        self.x = whiteBall.x + whiteBall.radius * zoom
        self.y = whiteBall.y
        self.visible = True

    def set_mouse(self, _mouse_x, _mouse_y):
        """Set the mouse position of...?

        Args:
            _mouse_x (int): x coordinate of the mouse position
            _mouse_y (int): y coordinate of the mouse position
        """
        if (self.move == False) and (self.xTarget == 0.0):
            self.mouse_x = _mouse_x
            self.mouse_y = _mouse_y

    def draw(self, whiteBall, table, zoom):
        """Draw the queue. There are three designs...

        Args:
            whiteBall (Ball): The position of the queue depends on the position of the white ball.
            table (Table): We need some informations about the table on which we are playing.
            zoom (float): Zoom factor to scale the window size. Scales also the ball size.
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

            # Design option 2
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

            # Design option 3
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

            # Draw target assistance
            if (self.visible == True) and (self.draw_target_assistance == True):

                if (self.move == 0) and (self.xTarget == 0):
                    cos_alpha = (self.mouse_x - whiteBall.x) / np.sqrt((self.mouse_x - whiteBall.x) ** 2 + (self.mouse_y - whiteBall.y) ** 2)
                    alpha = np.arccos(cos_alpha)

                    if whiteBall.y > self.mouse_y:
                        alpha = -alpha

                    gameboardwidth = table.gameboardwidth
                    gameboardheight = table.gameboardheight
                    border = table.border

                    yTargethelp = gameboardheight
                    xTargethelp = (self.x * yTargethelp) / self.y

                    d = np.sqrt(yTargethelp ** 2 + xTargethelp ** 2)

                    length = 3000

                    # Comment...
                    x1 = whiteBall.x  # - whiteBall.radius ?
                    y1 = whiteBall.y
                    x2 = self.x - whiteBall.radius - np.cos(alpha) * length
                    y2 = self.y + np.sin(-alpha) * length
                    x3 = x2
                    y3 = y2

                    # Cases for reflection of the target assistance ray
                    if y2 > gameboardheight - border:
                        m = (y2 - y1) / (x2 - x1)
                        delta_x = (gameboardheight - border - y1) / m

                        x2 = x1 + delta_x
                        y2 = gameboardheight - border

                        if delta_x > 0:
                            x3 = x2 + length
                            y3 = y2 - m * length
                        else:
                            x3 = x2 - length
                            y3 = y2 + m * length

                    if y2 < border:
                        m = (y2 - y1) / (x2 - x1)
                        delta_x = (border - y1) / m

                        x2 = x1 + delta_x
                        y2 = border

                        if delta_x < 0:
                            x3 = x2 - length
                            y3 = y2 + m * length
                        else:
                            x3 = x2 + length
                            y3 = y2 - m * length

                    if x2 > gameboardwidth - border:
                        m = (x2 - x1) / (y2 - y1)
                        delta_y = (gameboardwidth - border - x1) / m

                        x2 = gameboardwidth - border
                        y2 = self.y + delta_y

                        if delta_y < 0:
                            x3 = x2 + m * length
                            y3 = y2 - length
                        else:
                            x3 = x2 - m * length
                            y3 = y2 + length

                    if x2 < border:
                        m = (x2 - x1) / (y2 - y1)
                        delta_y = (border - x1) / m

                        x2 = border
                        y2 = y1 + delta_y

                        if delta_y < 0:
                            x3 = x2 + m * length
                            y3 = y2 - length
                        else:
                            x3 = x2 - m * length
                            y3 = y2 + length

                    if y3 > gameboardheight - border:
                        m = (y3 - y2) / (x3 - x2)
                        delta_x = (gameboardheight - border - y2) / m

                        x3 = x2 + delta_x
                        y3 = gameboardheight - border

                    if y3 < border:
                        m = (y3 - y2) / (x3 - x2)
                        delta_x = (border - y2) / m

                        x3 = x2 + delta_x
                        y3 = border

                    if x3 > gameboardwidth - border:
                        m = (x3 - x2) / (y3 - y2)
                        delta_y = (gameboardwidth - border - x2) / m

                        x3 = gameboardwidth - border
                        y3 = y2 + delta_y

                    if x3 < border:
                        m = (x3 - x2) / (y3 - y2)
                        delta_y = (border - x2) / m

                        x3 = border
                        y3 = y2 + delta_y

                    # Draw the line of the target assistance
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

    def hit(self, whiteBall, t):
        """Function that hits the white ball.

        Args:
            whiteBall (Ball): We need the position of the white ball.
            t (float): Time difference in seconds.
        """
        if (self.visible == True) and (self.move == True):
            if self.xTarget < self.xTargetMax:
                self.x += self.v * t
                self.xTarget += self.v * t

        if (self.visible == True) and (self.move == False):
            if self.xTarget > 0:
                self.xTarget -= self.v * t
                self.x -= self.v * t
                self.v += self.a * t

                if self.xTarget <= 0:  # The ball is hit

                    self.x -= self.xTarget
                    self.xTarget = 0

                    cos_alpha = (self.mouse_x - whiteBall.x) / np.sqrt((self.mouse_x - whiteBall.x) ** 2 + (self.mouse_y - whiteBall.y) ** 2)
                    alpha = np.arccos(cos_alpha)

                    if whiteBall.y > self.mouse_y:
                        alpha = -alpha

                    whiteBall.vx = -self.v * np.cos(alpha)
                    whiteBall.vy = -self.v * np.sin(alpha)

                    self.v = self.v_reset
                    self.visible = False

    def queuestrength(self, table):
        """Draw an indicator of the strength of the queue hit. Displayed on the right.

        Args:
            table (Table): Get table size.
        """
        gameboardwidth = table.gameboardwidth
        gameboardheight = table.gameboardheight

        balkeny = (self.xTarget * (gameboardheight - 140) / self.xTargetMax) + 70

        glEnable(GL_TEXTURE_2D)  # enable 2d texture
        glBindTexture(GL_TEXTURE_2D, self.texture)  # which texture to use
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(gameboardwidth, balkeny)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(gameboardwidth, balkeny + 2000)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(gameboardwidth + 300, balkeny + 2000)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(gameboardwidth + 300, balkeny)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(gameboardwidth, balkeny)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(gameboardwidth, balkeny + 10)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(gameboardwidth + 300, balkeny + 10)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(gameboardwidth + 300, balkeny)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glBegin(GL_POLYGON)
        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(gameboardwidth + 200, 65)
        glVertex2f(gameboardwidth + 70, 65)
        glVertex2f(gameboardwidth + 70, 70)
        glVertex2f(gameboardwidth + 200, 70)
        glEnd()

    def balkenzeichnen(self, table):
        """Draw sth...

        Args:
            table (Table): Get table size.
        """
        gameboardwidth = table.gameboardwidth
        gameboardheight = table.gameboardheight

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(gameboardwidth, 0)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(gameboardwidth, gameboardheight)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(gameboardwidth + 300, gameboardheight)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(gameboardwidth + 300, 0)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glBegin(GL_POLYGON)
        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(gameboardwidth + 200, 70)
        glColor3f(1.0, 0.0, 0.0)
        glVertex2f(gameboardwidth + 200, gameboardheight - 70)
        glColor3f(1.0, 0.0, 0.0)
        glVertex2f(gameboardwidth + 70, gameboardheight - 70)
        glColor3f(0.0, 1.0, 0.0)
        glVertex2f(gameboardwidth + 70, 70)
        glEnd()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glEnable(GL_BLEND)
        glBlendFunc(GL_DST_COLOR, GL_SRC_COLOR)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(gameboardwidth, 0)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(gameboardwidth, gameboardheight)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(gameboardwidth + 300, gameboardheight)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(gameboardwidth + 300, 0)
        glEnd()
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)

        self.queuestrength(table)

    def draw_shadow(self, whiteBall, zoom):
        """Draw the shadow of the queue.

        Args:
            whiteBall (Ball): ....
            zoom (float): Zoom factor to scale the window size. Scales also the ball size.
        """
        if self.visible == True:
            cos_alpha = (self.mouse_x - whiteBall.x) / np.sqrt((self.mouse_x - whiteBall.x) ** 2 + (self.mouse_y - whiteBall.y) ** 2)
            alpha = np.arccos(cos_alpha)

            if whiteBall.y > self.mouse_y:
                alpha = -alpha

            glPushMatrix()
            glTranslatef(self.x_shadow, self.y_shadow, 0.0)
            glTranslatef(whiteBall.x, whiteBall.y, 0.0)
            glScalef(1.0 / zoom, 1.0 / zoom, 1.0 / zoom)
            glRotatef(alpha * 180.0 / np.pi, 0.0, 0.0, 1.0)
            glTranslatef(-whiteBall.x, -whiteBall.y, 0.0)

            glEnable(GL_BLEND)
            glBlendFunc(GL_DST_COLOR, GL_SRC_COLOR)
            glColor3f(0.3, 0.3, 0.3)

            # Draw shadow for queue design 1
            if self.design == 1:
                glBegin(GL_QUADS)
                glVertex2f(self.x, self.y + 2)
                glVertex2f(self.x + 2, self.y + 2)
                glVertex2f(self.x + 2, self.y - 2)
                glVertex2f(self.x, self.y - 2)

                glVertex2f(self.x + 2, self.y + 2)
                glVertex2f(self.x + 2, self.y - 2)
                glVertex2f(self.x + 15, self.y - 3)
                glVertex2f(self.x + 15, self.y + 3)

                glVertex2f(self.x + 15, self.y + 3)
                glVertex2f(self.x + 15, self.y - 3)
                glVertex2f(self.x + 200, self.y - 5)
                glVertex2f(self.x + 200, self.y + 5)

                """
                glVertex2f(self.x + 80, self.y)
                glVertex2f(self.x + 80, self.y)
                glVertex2f(self.x + 200, self.y - 5)
                glVertex2f(self.x + 200, self.y + 5)
                """
                glVertex2f(self.x + 200, self.y - 5)
                glVertex2f(self.x + 200, self.y + 5)
                glVertex2f(self.x + 400, self.y + 6)
                glVertex2f(self.x + 400, self.y - 6)
                glEnd()

            # Draw shadow for queue design 2
            if self.design == 2:
                queuetop = 5
                queuelength = 400
                queueend = 10

                glBegin(GL_QUADS)
                glVertex2f(self.x, self.y - queuetop / 2)
                glVertex2f(self.x, self.y + queuetop / 2)
                glVertex2f(self.x + queuelength, self.y + queueend / 2)
                glVertex2f(self.x + queuelength, self.y - queueend / 2)
                glEnd()

                """
                glBegin(GL_QUADS)
                glVertex2f(self.x, self.y - queuetop / 2)
                glVertex2f(self.x, self.y + queuetop / 2)
                glVertex2f(self.x + 2, self.y + queuetop / 2)
                glVertex2f(self.x + 2, self.y - queuetop / 2)
                glEnd()
                """

            # Draw shadow for queue design 3
            if self.design == 3:
                queuetop = 20
                queuelength = 270
                queueend = 20

                # yellow rectangle
                glBegin(GL_QUADS)

                glVertex2f(self.x + 30, self.y - queuetop / 2)
                glVertex2f(self.x + 30, self.y + queuetop / 2)

                glVertex2f(self.x + queuelength, self.y + queueend / 2)
                glVertex2f(self.x + queuelength, self.y - queueend / 2)

                """
                # black stripe
                glBegin(GL_QUADS)
                glVertex2f(x + 30, y - queuetop / 4)
                glVertex2f(x + 30, y + queuetop / 4)
                glVertex2f(x + queuelength, y + queueend / 4)
                glVertex2f(x + queuelength, y - queueend / 4)
                """

                # red end
                glBegin(GL_QUADS)
                glVertex2f(self.x + queuelength, self.y - queuetop / 1.9)
                glVertex2f(self.x + queuelength, self.y + queuetop / 1.9)
                glVertex2f(self.x + queuelength + 5.5, self.y + queueend / 2.8)
                glVertex2f(self.x + queuelength + 5.5, self.y - queueend / 2.8)

                # brown top
                glBegin(GL_QUADS)
                glVertex2f(self.x, self.y)
                glVertex2f(self.x, self.y)
                glVertex2f(self.x + 30, self.y + queuetop / 2)
                glVertex2f(self.x + 30, self.y - queuetop / 2)

                """
                # gray top
                glBegin(GL_QUADS)
                glVertex2f(self.x, self.y)
                glVertex2f(self.x, self.y)
                glVertex2f(self.x + 10, self.y + queuetop / 4.5)
                glVertex2f(self.x + 10, self.y - queuetop / 4.5)

                # small brown triangle 1
                glBegin(GL_QUADS)
                glVertex2f(self.x + 30, self.y + queuetop / 2)
                glVertex2f(self.x + 30, self.y)
                glVertex2f(self.x + 35, self.y + queuetop / 4)
                glVertex2f(self.x + 35, self.y + queuetop / 4)

                # small brown triangle 2
                glBegin(GL_QUADS)
                glVertex2f(self.x + 30, self.y - queuetop / 2)
                glVertex2f(self.x + 30, self.y)
                glVertex2f(self.x + 35, self.y - queuetop / 4)
                glVertex2f(self.x + 35, self.y - queuetop / 4)
                """

                glEnd()

            glPopMatrix()
            glDisable(GL_BLEND)
