from math import *
from random import *
from pyray import *
import numpy as np

width = 800
height = 600
init_window( width, height, "window")

cameraX = 1
cameraY = 1
cameraZ = 0.7
scroll = 0.05
mode = 0
drawing = False
playing = True
damp = 0.98

G = 50

class Planet():
    def __init__(self, x, y, size, density, style):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.size = size
        self.density = density
        self.style = style
        self.id = random()
    def draw(self):
        circle( self.x, self.y, self.size, self.style)
    def drawV(self):
        line( self.x, self.y, self.x+self.vx*10, self.y+self.vy*10, GREEN)
    def update(self, planets):
        self.x += self.vx
        self.y += self.vy
        for planet in planets:
            if planet.id != self.id:
                if np.hypot(planet.x-self.x, planet.y-self.y) < planet.size+self.size:
                    #literally just stolen from https://github.com/xnx/collision/blob/master/collision.py idfk whats going on
                    m1, m2 = planet.size*planet.density, self.size*self.density
                    M = m1 + m2
                    r1, r2 = planet.size, self.size
                    d = pow(np.linalg.norm(r1 - r2), 2)
                    if d == 0:
                        d = 0.1
                    v1, v2 = np.array((planet.vx, planet.vy)), np.array((self.vx, self.vy))
                    u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
                    u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
                    planet.vx = u1[0] * damp
                    planet.vy = u1[1] * damp
                    self.vx = u2[0] * damp
                    self.vy = u2[1] * damp
                    

def circle( x, y, r, color):
    draw_circle( int(( x+cameraX)*cameraZ + width/2), int(( y+cameraY)*cameraZ + height/2), r*cameraZ+1, color)
def line( x1, y1, x2, y2, color):
    draw_line( int((x1+cameraX)*cameraZ + width/2), int((y1+cameraY)*cameraZ + height/2), int(( x2+cameraX)*cameraZ + width/2), int((y2+cameraY)*cameraZ + height/2), color)
def text( text, x, y, size, color):
    draw_text( text, int(( x+cameraX)*cameraZ + width/2), int(( y+cameraY)*cameraZ + height/2), int(size*cameraZ+1), color)
def fix(planets):
    for A in planets:
        A.update(planets)
        for B in planets:
            if A.id != B.id:
                d = sqrt( pow( B.x - A.x, 2 )+pow( B.y - A.y, 2 ))
                if d < A.size + B.size:
                    e = A.size + B.size - d
                    a = atan2(B.y-A.y,B.x-A.x)
                    dx = cos(a) * e/2
                    dy = sin(a) * e/2
                    A.x -= dx
                    A.y -= dy
                    B.x += dx
                    B.y += dy
stars = []
for i in range(300):
    stars.append([ randint( -width, width*2), randint( -height, height*2), random()+0.5])

planets = []
for i in range(60):
    planets.append(Planet( randint( -1500, 1500), randint( -1500, 1500), randint( 10, 50), random()+1, Color( randint( 50, 200), randint( 50, 200), randint( 50, 200), 255)))
for i in range(5):
    planets.append(Planet( randint( -1500, 1500), randint( -1500, 1500), randint( 60, 130), random()+1, YELLOW))

set_target_fps(60)

while not window_should_close():
    if is_key_pressed(KEY_SPACE):
        playing = not playing
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
    if mode == 1:
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            drawing = True
            startX = ((get_mouse_x() - width/2)/cameraZ)-cameraX
            startY = ((get_mouse_y() - height/2)/cameraZ)-cameraY
        if is_mouse_button_released(MOUSE_BUTTON_LEFT):
            drawing = False
            endX = ((get_mouse_x() - width/2)/cameraZ)-cameraX
            endY = ((get_mouse_y() - height/2)/cameraZ)-cameraY
            planets.append(Planet( startX, startY, 1500, random()+1, Color( randint( 50, 200), randint( 50, 200), randint( 50, 200), 255)))
            planets[-1].vx = (endX - startX)*cameraZ / 10
            planets[-1].vy = (endY - startY)*cameraZ / 10
    if mode == 2:
        if is_mouse_button_down(MOUSE_BUTTON_LEFT):
            for i in range(len(planets)):
                if sqrt( pow(planets[i].x-(((get_mouse_x() - width/2)/cameraZ)-cameraX), 2) + pow(planets[i].y-(((get_mouse_y() - height/2)/cameraZ)-cameraY), 2) ) <= planets[i].size:
                    planets.pop(i)
                    break
    if playing:
        fix(planets)
        fix(planets)
        fix(planets)
        for A in planets:
            A.update(planets)
            for B in planets:
                if A.id != B.id:
                    d = sqrt( pow( B.x - A.x, 2 )+pow( B.y - A.y, 2 ))
                    if d > A.size + B.size:
                        a = atan2(B.y-A.y,B.x-A.x)
                        force = ( G * A.size * B.size * A.density * B.density ) / pow( d, 2)
                        dx = cos(a)*force
                        dy = sin(a)*force
                        A.vx += dx / A.size * A.density
                        A.vy += dy / A.size * A.density

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
    if drawing == True:
        line( startX, startY, ((get_mouse_x() - width/2)/cameraZ)-cameraX, ((get_mouse_y() - height/2)/cameraZ)-cameraY, WHITE)
    if not playing:
        draw_rectangle( width-20, 20, 5, 20, WHITE)
        draw_rectangle( width-31, 20, 5, 20, WHITE)
    end_drawing()

close_window()