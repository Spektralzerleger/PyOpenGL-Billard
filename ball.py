'''
Last modified: 18.06.2020
here we define the ball class ...
'''

from graphics import *
from table import *
from textures import *


# First some help functions

# create random matrix
def random_matrix():
    # random angles
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
    # glLoadIdentity()

'''
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
'''

potted_stripes = 0
potted_solids = 0


class Ball:
    def __init__(self, _x, _y, _radius, _vx, _vy, _r, _g, _b, _m, _number):
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
        
        self.visible = True
        self.potted = False
        self.shift = False
        self.phi = 0.0
        # self.d = 0
        # Textur = 0
        
        '''
        if Textur == 0:
            char dateiname[255];
            sprintf(dateiname, "Texturen/%i.bmp", zahl); 
            Textur = LadeTextur(dateiname); 
        '''
        
        random_matrix()
        
        self.x_shadow = 10
        self.y_shadow = -6


    def move(self, t):
        if self.visible:
            self.x += self.vx * t
            self.y += self.vy * t
            
            v_norm = np.sqrt(self.vx**2 + self.vy**2) # could also define this in init
            self.phi = t * v_norm / self.radius
            
            glPushMatrix()
            glLoadIdentity()
            
            if v_norm > 0.0:
                glRotatef(self.phi * 180.0 / np.pi, -self.vy / v_norm, self.vx / v_norm, 0.0)
                glMultMatrixd(matrix) # evtl. mit glMatrixMode(GL_MODELVIEW) wie oben
                glGetDoublev(GL_MODELVIEW_MATRIX, matrix) # pyopengl works differently, matrix?
                
            glPopMatrix()
            
            # friction
            if v_norm > 0.0:
                v_prime_norm = v_norm - 68 * t  # tune this parameter for real effect
                
                if v_prime_norm < 0.0:
                    v_prime_norm = 0.0
                    
                self.vx *= v_prime_norm / v_norm
                self.vy *= v_prime_norm / v_norm
            
            # return true

        # return false
            
        
        
    def draw(self):
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

                '''
                char str[10]
                sprintf(str, "%i%", zahl)
                if self.number < 10:
                    graphicsText(x - 2, y - 3.5, str)
                else:
                    graphicsText(x - 4.5, y - 3.5, str)  # hier brauch ichs doch...
                '''
                
    def draw3d(self, zoom):
        # for "disappearing" animation
        # for all balls exept white and black 
        if ((self.number == 0 and not self.visible) or (self.number == 8 and not self.visible)) == False:

            # set position of light source 
            light_position = [zoom * (self.x - 200.0), zoom * (self.y + 200.0), zoom * 200.0, 1.0]
            light_direction = [zoom * self.x, zoom * self.y, 0.0, 1.0]

            glLightfv(GL_LIGHT0, GL_POSITION, light_position)
            glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, light_direction)

            # turn on textures
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, Textur) ### fix

            # here we move, rotate and draw the ball
            glPushMatrix()
            glScalef(zoom, zoom, zoom)
            glTranslatef(self.x, self.y, 0.0)
            glMultMatrixd(matrix)
            if self.radius > 1.0:
                graphicsBall3D(self.radius)
            glPopMatrix()

            # turn off textures
            glDisable(GL_TEXTURE_2D)


'''
    def collision(table, t):
        width = table.get_gameboardwidth()
        height = table.get_gameboardheight()
        border = table.get_border()

        friction = 0.75

        if potted != True:
            if ((x + radius > breite - border) || (x - radius < border)) {
                vx = -vx;
                vx *= reibung;
                vy *= reibung;
                bewegen(t);
            }

            if((y + radius > hoehe - border) || (y - radius < border)) {
                vy = -vy;
                vx *= reibung;
                vy *= reibung;
                bewegen(t);

        disappear(table, t)

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
   
...
missing ...
             
'''