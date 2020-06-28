"""
Last modified: 28.06.2020

The ball class is defined here. All the important informations of a ball are stored here.
"""

from graphics import *
from table import *
from textures import *


# First some help functions

# Create random matrix
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
    matrix = glGetDoublev(GL_MODELVIEW_MATRIX)  # ??
    glPopMatrix()

    glPopMatrix()
    #glLoadIdentity() ??
    return matrix


"""
def set_matrix():
    theta1 = -90
    theta2 = 105

    if self.number > 8:
        theta2 = 75

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glPushMatrix()
    glRotatef(theta2, 0.0, 1.0, 0.0)
    glRotatef(theta1, 1.0, 0.0, 0.0)
    # glRotatef(theta3, 0.0, 0.0, 1.0)
    glGetDoublev(GL_MODELVIEW_MATRIX)
    glPopMatrix()

    glPopMatrix()
    # glLoadIdentity()
"""

potted_stripes = 0
potted_solids = 0


class Ball:
    def __init__(self, _x, _y, _radius, _vx, _vy, _r, _g, _b, _m, _number):
        """Define a ball.

        Args:
            _x (int): x coordinate of the balls center position
            _y (int): y coordinate of the balls center position
            _radius (float): Radius of the ball
            _vx (float): x component of the balls velocity
            _vy (float): y component of the balls velocity
            _r ([type]): [description] ?
            _g ([type]): [description] ?
            _b ([type]): [description] ?
            _m ([type]): [description] ?
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

        # Comment....
        self.visible = True
        self.potted = False
        self.shift = False
        self.phi = 0.0
        #self.d = 0
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
        if self.visible:
            self.x += self.vx * t
            self.y += self.vy * t

            v_norm = np.sqrt(self.vx ** 2 + self.vy ** 2)
            self.phi = t * v_norm / self.radius

            glPushMatrix()
            glLoadIdentity()

            if v_norm > 0.0:
                glRotatef(self.phi * 180.0 / np.pi, -self.vy / v_norm, self.vx / v_norm, 0.0)
                glMultMatrixd(self.matrix)
                self.matrix = glGetDoublev(GL_MODELVIEW_MATRIX)

            glPopMatrix()

            # Friction!!!
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

                """
                char str[10]
                sprintf(str, "%i%", zahl)
                if self.number < 10:
                    graphicsText(x - 2, y - 3.5, str)
                else:
                    graphicsText(x - 4.5, y - 3.5, str)  # hier brauch ichs doch...
                """

    def draw3d(self, zoom):
        """Draw the 3D ball...

        Args:
            zoom (int): Zoom factor to scale the window size. Scales also the ball size.
        """        
        # For "disappearing" animation
        # For all balls exept white and black
        if ((self.number == 0 and self.visible == False) or (self.number == 8 and self.visible == False)) == False:

            # Set position of light source because it depends on the position of the ball
            light_position = [zoom * (self.x - 200.0), zoom * (self.y + 200.0), zoom * 200.0, 1.0]
            light_direction = [zoom * self.x, zoom * self.y, 0.0, 1.0]

            glLightfv(GL_LIGHT0, GL_POSITION, light_position)
            glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, light_direction)

            # Turn on textures
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)  ### fix ??

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

    def collision(self, table, t):  # vielleicht umbennen in ball_table_collision...
        width = table.gameboardwidth
        height = table.gameboardheight
        border = table.border

        friction = 0.75

        if self.potted == False:
            if (self.x + self.radius > width - border) or (self.x - self.radius < border):
                self.vx = -self.vx
                self.vx *= friction
                self.vy *= friction
                self.move(t)

            if (self.y + self.radius > height - border) or (self.y - self.radius < border):
                self.vy = -self.vy
                self.vx *= friction
                self.vy *= friction
                self.move(t)

        # disappear(table, t)

    """
    counter = 0
    def disappear(table, t):
        hole_radius_middle = table.get_hole_radius_middle()
        hole_radius_edges = table.get_hole_radius_edges()
        gameboard_width = table.get_gameboard_width()
        gameboard_height = table.get_gameboard_height()
        border = table.get_border()

        d = np.zeros(6)

        # upper right
        d[0] = np.sqrt(((gameboard_width - border)-(self.x))*((gameboard_width - border)-(self.x))+((gameboard_height - border)-(self.y))*((gameboard_height - border)-(self.y)))
        # lower right
        d[1] = np.sqrt(((gameboard_width - border)-(self.x))*((gameboard_width - border)-(self.x))+((0 + border)-(self.y))*((0 + border)-(self.y)))
        # lower left
        d[2] = np.sqrt(((0 + border)-(self.x))*((0 + border)-(self.x))+((0 + border)-(self.y))*((0 + border)-(self.y)))
        # upper left
        d[3] = np.sqrt(((0 + border)-(self.x))*((0 + border)-(self.x))+((gameboard_height - border)-(self.y))*((gameboard_height - border)-(self.y)))
        # upper middle
        d[4] = np.sqrt(((gameboard_width / 2)-(self.x))*((gameboard_width / 2)-(self.x))+((border)-(self.y))*((border)-(self.y)))
        # lower middle
        d[5] = np.sqrt(((gameboard_width / 2)-(self.x))*((gameboard_width / 2)-(self.x))+((gameboard_height - border)-(self.y))*((gameboard_height - border)-(self.y)))
            
        # changes in "disappear"
        for i in range(4):    # holes on edges
            if d[i] < hole_radius_edges:
                potted = True

        for j in range(4, 6):
            if d[j] < hole_radius_middle: # holes in middle
                potted = True

        if potted and visible:      
            self.radius -= 0.04 * 2000 * t
            counter ++; # increase by 1
        //std::cout << radius << " "  << zaehler << std::endl; 

        v_norm = np.sqrt(self.vx**2 + self.vy**2)
        v_prime_norm = v_norm - 50000 * t
                
        if v_prime_norm < 0.0:
            v_prime_norm = 0.0

        if v_norm > 0.0:
            self.vx *= v_prime_norm / v_norm
            self.vy *= v_prime_norm / v_norm

        std::cout << v_betrag << " " << v_strich_betrag << std::endl;
            
        //cout << eingelocht << endl;
            
        if self.radius < 1:
  
            visible = False
            if self.number != 8:
                self.radius = 29.1    
                self.vy = 0.0 

            set_matrix();

            if self.number == 0:
                self.vx = 0.0

            elif self.number == 8:
                self.vx = 0.0

            elif self.number > 8  # stripes roll in from the right
                self.vx = -300
                self.x = 3015 - self.radius
                self.y = 1545

            else:  # solids roll in from the left
                self.vx = 300
                self.x = self.radius
                self.y = 1545
   

        missing ...      
        """

    def draw_shadow(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_DST_COLOR, GL_SRC_COLOR)

        glColor3f(0.3, 0.3, 0.3)

        if self.visible:
            graphicsBall(self.x + self.x_shadow, self.y + self.y_shadow, 1.2 * self.radius)

        glDisable(GL_BLEND)
