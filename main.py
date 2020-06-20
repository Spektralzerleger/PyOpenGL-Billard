from graphics import *
from table import *
# from ball import *
from textures import *


'''
Rewrite this C++ Code into Python!!!
'''


'''
// FORWARD-DEKLARATIONEN:
void initKugeln(); ??
'''

# gameboard and window size
border = 100
width = 2540 + 2 * border
height = 1270 + 2 * border

holesize_middle = 69.85
holesize_edges = 92.70
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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # table and queue
    table = Table(width, height, border, 0.5, 0.0, 0.0, 0.0, 0.5, 0.0, holesize_middle, holesize_edges, 0.0, 0.0, 0.0, load_texture("Textures/tisch.bmp"), load_texture("Textures/balken.bmp"), 0)
    #queue = Queue()

    table.draw()
    
    '''
    queue.balkenzeichnen(tisch)

    for(int i = 0; i < N; i++)
    kugel[i].schatten_zeichnen();

    queue.schatten_zeichnen(kugel[0], zoom)

    graphicsEnable3D(window_width, window_height)

    for(int i = 0; i < N; i++)
    kugel[i].zeichnen3d(zoom)

    graphicsDisable3D(window_width, window_height, zoom)

    queue.zeichnen(kugel[0], tisch, zoom)

    if(! kugel[8].get_sichtbar()) {
    gameover = True;
    tisch.zeichneGameover() 
    }
    '''
    glFlush()
    glutSwapBuffers()

'''
void idle() {
     
  t = t + diff_seconds();
  if(t > 0.25)
    t = 0.0;
  
  while(t > takt && ! gameover) {
          
    int stehen = 0;      
      
    for(int i = 0; i < N; i++)  
      if(kugel[i].bewegen(takt) == false)
        stehen ++;         
 
    if(stehen == N) {
              
      if(! kugel[0].get_sichtbar() ){
        kugel[0].set_x(600); 
        kugel[0].set_y(hoehe / 2);  
        kugel[0].set_sichtbar(true);
        kugel[0].set_eingelocht(false);
        kugel[0].set_radius(kugelRadius);
        kugel[0].set_verschieben(true);
      }
      if(! kugel[0].get_eingelocht())
        queue.init_position(kugel[0], zoom); 
    }
   
    for(int i = 0; i < N; i++) {
      kugel[i].kollision(tisch, takt);
      kugel[i].ausrollen(takt);
    }
    
    for(int i = 0; i < N; i++)
      for(int j = i + 1; j < N; j++)
        kugel[i].stossen(kugel[j], takt);  
    
    queue.anstossen(kugel[0], takt);
        
    t -= takt;
  }
      
  display();     
}

// Wird aufgerufen, wenn eine Taste gedrückt wird:
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
  
// Wird aufgerufen, wenn eine Maustaste gedrückt wird:
void mouse(int button, int state, int x, int y) {
     
   //cout << "Eine Maustaste wurde an der Position " << x << " " << hoehe - y << " gedrueckt!" << endl;    
     
   if(state == GLUT_DOWN) {
     kugel[0].set_verschieben(false);
     queue.set_bewegung(true);
   }
     
   if(state == GLUT_UP)
     queue.set_bewegung(false);  
}


// Wird aufgerufen, wenn die Maus bewegt wird:
void mouseMotion(int x, int y) {
    
  queue.set_mouse(int(x / zoom), int((fensterHoehe - y) / zoom)); 

}

// Die Funktion wird aufgerufen, wenn sich die Größe des Bildschirms ändert:
void reshape(int width, int height) {
     
  glutReshapeWindow(fensterBreite, fensterHoehe);   

}

void initKugeln() {
     
  // Die Arrays geben die nummer der Kugeln an Bsp: Kugel [8] = schwarze 8: 
  kugel[0].init(600, hoehe / 2, kugelRadius, 0.0, 0.0, 1.0, 1.0, 1.0, 10, 0);
  //kugel[1].init(200, 200, kugelRadius, 0.0, 0.0, 1.0, 0.8, 0.0, 10, 1);
  kugel[1].init(1815, hoehe / 2, kugelRadius, 0.0, 0.0, 1.0, 0.8, 0.0, 10, 1);
  kugel[2].init(1870 + 55, hoehe / 2 + 70, kugelRadius, -0.0, 0.0, 0.0, 0.0, 0.67, 10, 2);
  kugel[3].init(1870 + 55, hoehe / 2 - 70, kugelRadius, -0.0, 0.0, 1.0, 0.0, 0.0, 10, 3);
  kugel[4].init(1870 +  3 *55, hoehe / 2 + 70, kugelRadius, -0.0, 0.0, 0.4, 0.0, 0.6, 10, 4);
  kugel[5].init(1870 +  3 *55, hoehe / 2 + 2 * 70, kugelRadius, -0.0, 0.0, 1.0, 0.5, 0.0, 10, 5); 
  kugel[6].init(1870 +  3 *55, hoehe / 2 - 70, kugelRadius, -0.0, 0.0, 0.2, 0.7, 0.2, 10, 6);
  kugel[7].init(1870 + 2 * 55, hoehe / 2 + 35, kugelRadius, -0.0, 0.0, 0.5, 0.0, 0.0, 10, 7);
  kugel[8].init(1870 + 55, hoehe / 2,kugelRadius, -0.0, 0.0, 0.0, 0.0, 0.0, 10, 8);
  //kugel[8].init(300 , 300,kugelRadius, -0.0, 0.0, 0.0, 0.0, 0.0, 10, 8);
  kugel[9].init(1870 +  3 *55, hoehe / 2, kugelRadius, -0.0, 0.0, 1.0, 0.8, 0.0, 10, 9);
  kugel[10].init(1870 +  3 *55, hoehe / 2 - 2 * 70, kugelRadius, -0.0, 0.0, 0.0, 0.0, 0.67, 10, 10);
  kugel[11].init(1870 +  2 *55, hoehe / 2 + 35 + 70, kugelRadius, -0.0, 0.0, 1.0, 0.0, 0.0, 10, 11);
  kugel[12].init(1870 +  2 *55 , hoehe / 2 - 35, kugelRadius, -0.0, 0.0, 0.4, 0.0, 0.6, 10, 12);
  kugel[13].init(1870 +  2 *55, hoehe / 2 - 35 - 70, kugelRadius, -0.0, 0.0, 1.0, 0.5, 0.0, 10, 13);
  kugel[14].init(1870, hoehe / 2 + 35, kugelRadius, -0.0, 0.0, 0.2, 0.7, 0.2, 10, 14);
  kugel[15].init(1870, hoehe / 2 - 35, kugelRadius, -0.0, 0.0, 0.5, 0.0, 0.0, 10, 15);
  
  gameover = false;

}

'''



def main():
    # initialize graphics:
    graphicsInit("Billard", width + 275, height + 150, zoom)
    graphicsInit3D(width, height)

    # register display function:
    glutDisplayFunc(display)

    '''
    # register idle function:
    glutIdleFunc(idle)

    # register keyboard function:
    glutKeyboardFunc(keyboard)

    # register mouse function
    glutMouseFunc(mouse)
    glutPassiveMotionFunc(mouseMotion)

    glutReshapeFunc(reshape)

    textureBalken = LadeTextur("Texturen/balken.bmp")

    tisch.init(breite, hoehe, bande, 0.5, 0.0, 0.0, 0.0, 0.5, 0.0, lochgroesseMitte, lochgroesseEcke, 0.0, 0.0, 0.0, LadeTextur("Texturen/tisch.bmp"), texturBalken, LadeTextur("Texturen/gameover.bmp"));    

    initKugeln()

    queue.init(100.0, 15000.0, texturBalken)
    queue.init_position(kugel[0], zoom)

    # time measurement:
    diff_seconds()   
    '''
            
    # show window:          
    glutMainLoop()


if __name__ == "__main__":
    main()