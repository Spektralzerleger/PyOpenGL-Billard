"""
Last modified: 11.07.2020

The ball class is defined here. All the important information of a ball are stored here.

FIX: More efficient rendering.
"""

from graphics import *
from table import *
from textures import *


# Help function for ball initialization
def random_matrix():
    """Function that creates a random matrix for initial ball position.

    Returns:
        matrix: Start configuration of ball
    """
    # Initialize random angles
    theta1 = np.random.rand() * 360
    theta2 = np.random.rand() * 360
    theta3 = np.random.rand() * 360

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glPushMatrix()
    glRotatef(theta1, 1.0, 0.0, 0.0)
    glRotatef(theta2, 0.0, 1.0, 0.0)
    glRotatef(theta3, 0.0, 0.0, 1.0)
    matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    glPopMatrix()
    glPopMatrix()
    return matrix


potted_stripes = 0
potted_solids = 0

counter = 0


class Ball:
    def __init__(self, _x, _y, _radius, _vx, _vy, _r, _g, _b, _m, _number):
        """Initialize a ball.

        Args:
            _x (int): x coordinate of the balls center position
            _y (int): y coordinate of the balls center position
            _radius (float): Radius of the ball
            _vx (float): x component of the balls velocity
            _vy (float): y component of the balls velocity
            _r ([type]): R value of the ball color for 2D image
            _g ([type]): G value of the ball color for 2D image
            _b ([type]): b value of the ball color for 2D image
            _m (float): Mass of the ball. For collision calculations.
            _number (int): Number of the ball. Defines also the texture.
        """
        self.x = _x
        self.y = _y
        self.radius = _radius
        self.vx = _vx
        self.vy = _vy
        self.r = _r
        self.g = _g
        self.b = _b
        self.m = _m
        self.number = _number

        # Private variables
        self.visible = True
        self.potted = False
        self.shift = False
        self.phi = 0.0
        self.texture = load_texture("Textures/{}.bmp".format(_number))

        """
        if Textur == 0:
            char dateiname[255];
            sprintf(dateiname, "Texturen/%i.bmp", zahl); 
            Textur = LadeTextur(dateiname); 
        """

        self.matrix = random_matrix()

        self.x_shadow = 10
        self.y_shadow = -6

    def move(self, t):
        """Function that defines how to move a ball.

        Args:
            t (float): Time parameter.

        Returns:
            bool: True, if ball still moves after time t. False, if not.
        """
        if self.visible == True:
            self.x += self.vx * t
            self.y += self.vy * t  # Maybe do this to the end?! Like in article https://gafferongames.com/post/integration_basics/

            v_norm = np.sqrt(self.vx ** 2 + self.vy ** 2)
            self.phi = t * v_norm / self.radius

            glPushMatrix()
            glLoadIdentity()

            if v_norm > 0.0:
                glRotatef(self.phi * 180.0 / np.pi, -self.vy / v_norm, self.vx / v_norm, 0.0)
                glMultMatrixd(self.matrix)
                self.matrix = glGetDoublev(GL_MODELVIEW_MATRIX)

            glPopMatrix()

            # Friction!!! Could do it as global parameter
            if v_norm > 0.0:
                v_prime_norm = v_norm - 68 * t  # tune this parameter for real effect

                if v_prime_norm < 0.0:
                    v_prime_norm = 0.0

                self.vx *= v_prime_norm / v_norm
                self.vy *= v_prime_norm / v_norm

                return True
        # Add comment
        return False

    def draw(self):
        """Draw a 2D ball...
        """
        if self.visible:
            glColor3f(self.r, self.g, self.b)
            graphicsBall(self.x, self.y, self.radius)

            if self.number <= 8:
                glColor3f(1.0, 1.0, 1.0)
            else:
                glColor3f(0.0, 0.0, 0.0)

            graphicsBall(self.x, self.y, self.radius / 2)

            if self.number > 0:
                if self.number > 8:
                    glColor3f(1.0, 1.0, 1.0)
                else:
                    glColor3f(0.0, 0.0, 0.0)

                if self.number < 10:
                    graphicsText(self.x - 2, self.y - 3.5, str(self.number))
                else:
                    graphicsText(self.x - 4.5, self.y - 3.5, str(self.number))

    def draw3d(self, zoom):
        """Draw the 3D ball with texture.

        Args:
            zoom (int): Zoom factor to scale the window size. Scales also the ball size.
        """
        # For "disappearing" animation
        # For all balls except white and black
        if ((self.number == 0 and self.visible == False) or (self.number == 8 and self.visible == False)) == False:

            # Set position of light source because it depends on the position of the ball
            light_position = [zoom * (self.x - 200.0), zoom * (self.y + 200.0), zoom * 200.0, 1.0]
            light_direction = [zoom * self.x, zoom * self.y, 0.0, 1.0]

            glLightfv(GL_LIGHT0, GL_POSITION, light_position)
            glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, light_direction)

            # Turn on textures
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)

            # Here we move, rotate and draw the ball
            glPushMatrix()
            glScalef(zoom, zoom, zoom)
            glTranslatef(self.x, self.y, 0.0)
            glMultMatrixd(self.matrix)
            if self.radius > 1.0:
                graphicsBall3D(self.radius)
            glPopMatrix()

            # Turn off textures
            glDisable(GL_TEXTURE_2D)

    def table_collision(self, table, t):
        # Get the table size
        width = table.gameboardwidth
        height = table.gameboardheight
        border = table.border

        # Elasticity
        friction = 0.75

        if self.potted == False:
            # Collision with the right table side
            if (self.x + self.radius > width - border) and (self.vx > 0):
                self.x = width - border - self.radius
                self.vx = -self.vx
                self.vx *= friction
                self.vy *= friction
                #self.move(t)

            # Collision with the left table side
            if (self.x - self.radius < border) and (self.vx < 0):
                self.x = border + self.radius
                self.vx = -self.vx
                self.vx *= friction
                self.vy *= friction
                #self.move(t)

            # Collision with the bottom of the table
            if (self.y + self.radius > height - border) and (self.vy > 0):
                self.y = height - border - self.radius
                self.vy = -self.vy
                self.vx *= friction
                self.vy *= friction
                #self.move(t)
            
            # Collision with the top of the table
            if (self.y - self.radius < border) and (self.vy < 0):
                self.y = border + self.radius
                self.vy = -self.vy
                self.vx *= friction
                self.vy *= friction
                #self.move(t)

        self.disappear(table, t)

    def disappear(self, table, t):
        """Define what happens when a ball is potted.

        Args:
            table (object): Initialized table on which the balls are moving
            t (float): Time variable
        """
        global counter
        # Get the table and hole size
        hole_radius_middle = table.holesize_middle
        hole_radius_edges = table.holesize_edges
        gameboard_width = table.gameboardwidth
        gameboard_height = table.gameboardheight
        border = table.border

        # List of the balls distance to the ith hole
        d = [0, 1, 2, 3, 4, 5]

        # upper right
        d[0] = np.sqrt(((gameboard_width - border) - (self.x)) ** 2 + ((gameboard_height - border) - (self.y)) ** 2)
        # lower right
        d[1] = np.sqrt(((gameboard_width - border) - (self.x)) ** 2 + ((0 + border) - (self.y)) ** 2)
        # lower left
        d[2] = np.sqrt(((0 + border) - (self.x)) ** 2 + ((0 + border) - (self.y)) ** 2)
        # upper left
        d[3] = np.sqrt(((0 + border) - (self.x)) ** 2 + ((gameboard_height - border) - (self.y)) ** 2)
        # upper middle
        d[4] = np.sqrt(((gameboard_width / 2) - (self.x)) ** 2 + ((border) - (self.y)) ** 2)
        # lower middle
        d[5] = np.sqrt(((gameboard_width / 2) - (self.x)) ** 2 + ((gameboard_height - border) - (self.y)) ** 2)

        for i in range(4):  # holes on edges
            if d[i] < hole_radius_edges:
                self.potted = True

        for j in range(4, 6):
            if d[j] < hole_radius_middle:  # holes in middle
                self.potted = True

        if (self.potted == True) and (self.visible == True):
            self.radius -= 0.04 * 2000 * t
            counter += 1  # increase by 1

            # Stop the ball
            v_norm = np.sqrt(self.vx ** 2 + self.vy ** 2)
            v_prime_norm = v_norm - 50000 * t

            if v_prime_norm < 0.0:
                v_prime_norm = 0.0

            if v_norm > 0.0:
                self.vx *= v_prime_norm / v_norm
                self.vy *= v_prime_norm / v_norm

            if self.radius < 1:
                self.visible = False

                if self.number != 8:
                    self.radius = 29.1  # parameter
                    self.vy = 0.0

                # Set the right initial position for rolling in
                self.matrix = self.set_matrix()

                if self.number == 0:
                    self.vx = 0.0

                if self.number == 8:
                    self.vx = 0.0

                elif self.number > 8:  # stripes roll in from the right
                    self.vx = -300
                    self.x = 3015 - self.radius
                    self.y = 1545

                else:  # solids roll in from the left
                    self.vx = 300
                    self.x = self.radius
                    self.y = 1545

    def ball_collision(self, otherBall, t):
        """Ball - ball collision.

        Args:
            otherBall (Ball): other ball
            t (float): time
        """
        if (self.potted == False) and (self.visible == True) and (otherBall.visible == True):

            # Distance between the two ball centers
            d = np.sqrt((self.x - otherBall.x) ** 2 + (self.y - otherBall.y) ** 2)

            if d <= (self.radius + otherBall.radius):
                # Parameters of the first ball
                m1 = self.m
                x1 = self.x; v1x = self.vx
                y1 = self.y; v1y = self.vy
                # Parameters of the second ball
                m2 = otherBall.m
                x2 = otherBall.x; v2x = otherBall.vx
                y2 = otherBall.y; v2y = otherBall.vy
                # -cos() and sin()
                d_0x = (x1 - x2) / np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                d_0y = (y1 - y2) / np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                # Factor
                k = (2 * (d_0x * (v2x - v1x) + d_0y * (v2y - v1y))) / (1 / m1 + 1 / m2)

                # Elasticity
                friction = 0.95  # could do it as global parameter
                v1x_prime = v1x + (k / m1) * d_0x
                v1y_prime = v1y + (k / m1) * d_0y
                v2x_prime = v2x - (k / m2) * d_0x
                v2y_prime = v2y - (k / m2) * d_0y
                
                # Set new position, such that the balls aren't inside each other anymore
                delta = self.radius + otherBall.radius - d
                self.x += delta * d_0x
                self.y += delta * d_0y

                # Set new velocities
                self.vx = v1x_prime * friction
                otherBall.vx = v2x_prime * friction
                self.vy = v1y_prime * friction
                otherBall.vy = v2y_prime * friction

                #self.move(t)
                #otherBall.move(t)

    def draw_shadow(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_DST_COLOR, GL_SRC_COLOR)

        glColor3f(0.3, 0.3, 0.3)

        if self.visible:
            graphicsBall(self.x + self.x_shadow, self.y + self.y_shadow, 1.2 * self.radius)

        glDisable(GL_BLEND)

    def roll_out(self, t):
        """if ball is potted, roll out on the top...

        Args:
        t (float): Time parameter.
        """
        global potted_stripes, potted_solids
        if (self.potted == True) and (self.vx != 0.0):

            self.x += self.vx * t
            v_norm = np.sqrt(self.vx ** 2 + self.vy ** 2)
            self.phi = t * v_norm / self.radius

            # Here we save the rotation of the ball
            glPushMatrix()
            glLoadIdentity()

            if v_norm > 0.0:
                glRotatef(self.phi * 180.0 / np.pi, -self.vy / v_norm, self.vx / v_norm, 0.0)
                glMultMatrixd(self.matrix)
                glGetDoublev(GL_MODELVIEW_MATRIX, self.matrix)

            glPopMatrix()

            if (self.number > 8) and (self.vx < 0.0) and (self.x <= 1440 + potted_stripes * (np.pi * self.radius)) and (self.visible == False):
                self.vx = 0.0
                self.x = 1440 + potted_stripes * (np.pi * self.radius)
                potted_stripes += 1

            if (self.number <= 8) and (self.number > 0) and (self.vx > 0.0) and (self.x >= 1300 - potted_solids * (np.pi * self.radius)) and (self.visible == False):
                self.vx = 0.0
                self.x = 1300 - potted_solids * (np.pi * self.radius)
                potted_solids += 1

    # Help function
    def set_matrix(self):
        """Function that sets the potted balls, so they appear face up.

        Returns:
            matrix: Start configuration of potted balls for rolling.
        """
        theta1 = -90
        theta2 = 105
        theta3 = 180

        if self.number > 8:
            theta2 = 75

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glPushMatrix()
        glRotatef(theta2, 0.0, 1.0, 0.0)
        glRotatef(theta1, 1.0, 0.0, 0.0)
        glRotatef(theta3, 0.0, 0.0, 1.0)
        matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        glPopMatrix()
        glPopMatrix()
        return matrix
