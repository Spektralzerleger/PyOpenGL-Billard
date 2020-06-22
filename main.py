from graphics import *
from mytime import *
from table import *
from ball import *
from textures import *


'''
Rewrite this C++ Code into Python!!!
'''

# gameboard and window size
border = 100
width = 2540 + 2 * border
height = 1270 + 2 * border

holesize_middle = 62
holesize_edges = 65
zoom = 0.4
ballRadius = 29.1

window_width = int((width + 275) * zoom)
window_height = int((height + 150) * zoom)

gameover = False

# UNITS: 1 corresponds to 1mm in reality

# number of balls - ball[0] is the white ball:
N = 16
# Kugel kugel[N]; ??? ball class

# time measurement
t = 0.0
takt = 0.0004



def display():
    #global table, ball
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    table.draw()

    '''
    queue.balkenzeichnen(tisch)
    '''
    for i in range(N):
        ball[i].draw_shadow()

    '''
    queue.schatten_zeichnen(kugel[0], zoom)
    '''
    graphicsEnable3D(window_width, window_height)
    for i in range(N):
        ball[i].draw3d(zoom)
    graphicsDisable3D(window_width, window_height, zoom)

    '''
    queue.zeichnen(kugel[0], tisch, zoom)

    if(! kugel[8].get_sichtbar()) {
    gameover = True;
    tisch.zeichneGameover() 
    }
    '''
    glFlush()
    glutSwapBuffers()


def idle():
    global t
    # timeflow
    t = t + diff_seconds()
    if t > 0.25:
        t = 0.0

    while (t > takt and gameover == False):
        stand = 0
        '''
        for i in range(N):
            if ball[i].move(takt) == False:
                stand += 1        

        if stand == N:
          
            if ball[0].visible == False:
                ball[0].x = 600
                ball[0].y = height / 2
                ball[0].visble = True
                ball[0].potted = False
                ball[0].radius = ballRadius
                ball[0].shift = True

            if ball[0].potted == False:
                queue.init_position(ball[0], zoom)

        for i in range(N):
            ball[i].kollision(table, takt)
            ball[i].ausrollen(takt)

        for i in range(N):
            for j in range(i+1, N):
                ball[i].stossen(balls[j], takt)

        queue.anstossen(kugel[0], takt)
        '''
        t -= takt

    display()


'''
# is called when a button is pressed
void keyboard(unsigned char key, int x, int y) {
     
  //cout << "Die Taste " << key << " wurde gedrueckt!" << endl;  
  
  if(key == 'm') {
     for(int i = 0; i < N; i++) {
       if(! kugel[i].get_eingelocht()) {
         kugel[i].set_vx(0.0);
         kugel[i].set_vy(0.0); 
       }    
     }  
  }   
  
  if(key == 'n') {
    initKugeln();
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
'''


def initBalls():
    global ball
    # number is the number of the ball, e.g. 8 = black 8
    ball = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    
    ball[0] = Ball(600, height / 2, ballRadius, 0.0, 0.0, 1.0, 1.0, 1.0, 10, 0)
    ball[1] = Ball(1815, height / 2, ballRadius, 0.0, 0.0, 1.0, 0.8, 0.0, 10, 1)
    ball[2] = Ball(1870 + 55, height / 2 + 70, ballRadius, -0.0, 0.0, 0.0, 0.0, 0.67, 10, 2)
    ball[3] = Ball(1870 + 55, height / 2 - 70, ballRadius, -0.0, 0.0, 1.0, 0.0, 0.0, 10, 3)
    ball[4] = Ball(1870 +  3 *55, height / 2 + 70, ballRadius, -0.0, 0.0, 0.4, 0.0, 0.6, 10, 4)
    ball[5] = Ball(1870 +  3 *55, height / 2 + 2 * 70, ballRadius, -0.0, 0.0, 1.0, 0.5, 0.0, 10, 5)
    ball[6] = Ball(1870 +  3 *55, height / 2 - 70, ballRadius, -0.0, 0.0, 0.2, 0.7, 0.2, 10, 6)
    ball[7] = Ball(1870 + 2 * 55, height / 2 + 35, ballRadius, -0.0, 0.0, 0.5, 0.0, 0.0, 10, 7)
    ball[8] = Ball(1870 + 55, height / 2,ballRadius, -0.0, 0.0, 0.0, 0.0, 0.0, 10, 8)
    ball[9] = Ball(1870 +  3 *55, height / 2, ballRadius, -0.0, 0.0, 1.0, 0.8, 0.0, 10, 9)
    ball[10] = Ball(1870 +  3 *55, height / 2 - 2 * 70, ballRadius, -0.0, 0.0, 0.0, 0.0, 0.67, 10, 10)
    ball[11] = Ball(1870 +  2 *55, height / 2 + 35 + 70, ballRadius, -0.0, 0.0, 1.0, 0.0, 0.0, 10, 11)
    ball[12] = Ball(1870 +  2 *55 , height / 2 - 35, ballRadius, -0.0, 0.0, 0.4, 0.0, 0.6, 10, 12)
    ball[13] = Ball(1870 +  2 *55, height / 2 - 35 - 70, ballRadius, -0.0, 0.0, 1.0, 0.5, 0.0, 10, 13)
    ball[14] = Ball(1870, height / 2 + 35, ballRadius, -0.0, 0.0, 0.2, 0.7, 0.2, 10, 14)
    ball[15] = Ball(1870, height / 2 - 35, ballRadius, -0.0, 0.0, 0.5, 0.0, 0.0, 10, 15)



def main():
    global table
    # initialize graphics:
    graphicsInit("Billard", width + 275, height + 150, zoom)
    graphicsInit3D(width, height)
    
    # load textures
    table_texture = load_texture("Textures/tisch.bmp")
    balken_texture = load_texture("Textures/balken.bmp")
    gameover_texture = load_texture("Textures/gameover.bmp")

    # table and queue
    table = Table(width, height, border, 0.5, 0.0, 0.0, 0.0, 0.5, 0.0, holesize_middle, holesize_edges, 0.0, 0.0, 0.0, table_texture, balken_texture, gameover_texture)
    #queue = Queue()

    initBalls()
    # register display function:
    glutDisplayFunc(display)

    # register idle function:
    glutIdleFunc(idle)

    '''
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
    '''
            
    # show window:          
    glutMainLoop()


if __name__ == "__main__":
    main()