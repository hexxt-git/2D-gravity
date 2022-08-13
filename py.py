from math import *
from random import *
from pyray import *

width = 800
height = 600
init_window( width, height, "window")

cameraX = 1
cameraY = 1
cameraZ = 0.9
scroll = 0.05
mode = 0

G = 20

class Planet():
    def __init__(self, x, y, vx, vy, size, style):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.style = style
        self.id = random()
    def draw(self):
        circle( self.x, self.y, self.size, self.style)
    def drawV(self):
        line( self.x, self.y, self.x+self.vx*3, self.y+self.vy*3, GREEN)
    def update(self, planets):
        self.x += self.vx
        self.y += self.vy
        for planet in planets:
            if planet.id != self.id:
                pass

def circle( x, y, r, color):
    draw_circle( int(( x+cameraX)*cameraZ + width/2), int(( y+cameraY)*cameraZ + height/2), r*cameraZ+1, color)
def line( x1, y1, x2, y2, color):
    draw_line( int((x1+cameraX)*cameraZ + width/2), int((y1+cameraY)*cameraZ + height/2), int(( x2+cameraX)*cameraZ + width/2), int((y2+cameraY)*cameraZ + height/2), color)
def text( text, x, y, size, color):
    draw_text( text, int(( x+cameraX)*cameraZ + width/2), int(( y+cameraY)*cameraZ + height/2), int(size*cameraZ+1), color)


stars = []
for i in range(300):
    stars.append([ randint( -width, width*2), randint( -height, height*2), random()+0.5])

planets = []
#planets.append( Planet( 5000, 5000, 1000, YELLOW))
#for i in range(10):
   # planets.append(Planet( randint( -width, width), randint( -height, height), randint( 30, 80), Color( randint( 50, 200), randint( 50, 200), randint( 50, 200), 255)))

set_target_fps(60)

while not window_should_close():
    if is_key_pressed(KEY_ENTER):
        mode += 1
        if mode > 2:
            mode = 0
    if mode == 0:
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            pmx = get_mouse_x()
            pmy = get_mouse_y()
        if is_mouse_button_down(MOUSE_BUTTON_LEFT):
            mxv = get_mouse_x() - pmx
            myv = get_mouse_y() - pmy
            pmx = get_mouse_x()
            pmy = get_mouse_y()
            cameraX += mxv * 0.8 / cameraZ
            cameraY += myv * 0.8 / cameraZ
        if get_mouse_wheel_move() > 0: # zoom in
            if cameraZ < 10000:
                cameraZ *= 1 + scroll
        if get_mouse_wheel_move() < 0: # zoom out
            if cameraZ > 0.0001:
                cameraZ *= 1 - scroll
        if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
            bugs[0].x = ((get_mouse_x() - width/2)/cameraZ)-cameraX
            bugs[0].y = ((get_mouse_y() - height/2)/cameraZ)-cameraY

        for A in planets:
            for B in planets:
                if A.id != B.id:
                    d = sqrt( pow( B.x - A.x, 2 )+pow( B.y - A.y, 2 ))
                    if d > A.size + B.size:
                        a = atan2(B.y-A.y,B.x-A.x)
                        f = ( G * A.size * B.size ) / pow( d, 2)
                        dx = cos(a)*f
                        dy = sin(a)*f
                        #circle( A.x, A.y, 2, GREEN)
                        #text( str(floor(a*100)/100), A.x, A.y, 30, GREEN)
                        #line( A.x, A.y, A.x+dx, A.y+dy, GREEN)
                        A.vx += dx / A.size
                        A.vy += dy / A.size
            A.update(planets)

    begin_drawing()
    clear_background(Color( 3, 3, 5, 255))

    for star in stars:
        draw_circle( int(star[0]+(cameraX*0.12)), int(star[1]+(cameraY*0.12)), star[2], WHITE)
    for planet in planets:
        planet.draw()

    if mode == 0:
        draw_text( 'movement', 15, 10, 30, WHITE)
    if mode == 1:
        draw_text( 'drawing', 15, 10, 30, WHITE)
    if mode == 2:
        draw_text( 'deleting', 15, 10, 30, WHITE)

    draw_rectangle( 0, 0, width, height, WHITE)
    planet1 = Planet( 50, 50, 30, 10, 50, RED)
    planet2 = Planet( 130, 110, -20, -50, 50, BLUE)
    planet1.draw()
    planet2.draw()
    planet1.drawV()
    planet2.drawV()
    a = atan2( planet2.y-planet1.y, planet2.x-planet1.x)


    end_drawing()

close_window()