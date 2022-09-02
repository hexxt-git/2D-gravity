from math import *
from random import *
from pyray import *
import numpy as np

width = 1200
height = 700
init_window( width, height, "2D gravity")

cameraX = 1
cameraY = 1
cameraZ = 0.5
scroll = 0.11
mode = 0
modes = ['settings','drawing','deleting','stats','orbiter','camera']
selected = 0
power = 5
drawing = False
playing = True
bounce = True
doMerge = False
simSpeed = 0.3
randomize = False
walls = False
wallsX = 1500
wallsY = 1000
G = 0.8
dt = 0
textFont = load_font("font.ttf")
selectedColor = Color( 55, 138, 34, 255)
orbited = 0
orbiter = 1
isFolllowing = False
followed = 0

def dot( vector1, vector2):
    return vector1.x*vector2.x + vector1.y*vector2.y
def vectorMultiply( vector, number):
    newVector = Vector2( vector.x*number, vector.y*number)
    return newVector
def vectorSubtract( vector1, vector2):
    newVector = Vector2( vector1.x-vector2.x, vector1.y-vector2.y)
    return newVector
def vectorReflect( vector1, vector2):
    if dot( vector2, vector2) != 0:
        reflected = vectorSubtract( vector1 , vectorMultiply( vector2, 2 * dot( vector1, vector2)/dot( vector2, vector2)))
    else:
        reflected = Vector2( 0, 0)
    return reflected
def mass(planet):
    return pow( planet.size, 2) * pi * planet.density
class Planet():
    def __init__(self, x, y, size, density, style):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.static = False
        self.size = size
        if density == 0:
            density = 0.01
        self.density = density
        self.style = style
        self.id = random()
    def draw(self):
        circle( self.x, self.y, self.size, Color(self.style[0], self.style[1], self.style[2], self.style[3]))
    def drawV(self):
        line( self.x, self.y, self.x+self.vx*10, self.y+self.vy*10, GREEN)
    def update(self, planets):
        self.x += self.vx * dt * simSpeed * 10 * (not self.static)
        self.y += self.vy * dt * simSpeed * 10 * (not self.static)
        if walls:
            if self.x-self.size <= -wallsX:
                self.vx *= -bounce
                self.x -= self.x + wallsX - self.size
            if self.y-self.size <= -wallsY:
                self.vy *= -bounce
                self.y -= self.y + wallsY - self.size
            if self.x+self.size >= wallsX:
                self.vx *= -bounce
                self.x -= self.x - wallsX + self.size
            if self.y+self.size >= wallsY:
                self.vy *= -bounce
                self.y -= self.y - wallsY + self.size
        for planet in planets:
            if planet.id != self.id:
                if np.hypot(planet.x-self.x, planet.y-self.y) < planet.size+self.size:
                    vector = Vector2( self.vx, self.vy)
                    normal = Vector2( self.x-planet.x, self.y-planet.y)
                    newVector = vectorReflect( vector, normal)
                    if not bounce:
                        newVector = vectorMultiply( newVector, 0.3)
                    self.vx = newVector.x
                    self.vy = newVector.y

def circle( x, y, r, color):
    draw_circle( int(( x+cameraX)*cameraZ + width/2), int(( y+cameraY)*cameraZ + height/2), r*cameraZ+1, color)
def circle_line( x, y, r, color):
    draw_circle_lines( int(( x+cameraX)*cameraZ + width/2), int(( y+cameraY)*cameraZ + height/2), r*cameraZ+1, color)
def line( x1, y1, x2, y2, color):
    draw_line( int((x1+cameraX)*cameraZ + width/2), int((y1+cameraY)*cameraZ + height/2), int(( x2+cameraX)*cameraZ + width/2), int((y2+cameraY)*cameraZ + height/2), color)
def text( text, x, y, size, color):
    draw_text( text, int(( x+cameraX)*cameraZ + width/2), int(( y+cameraY)*cameraZ + height/2), int(size*cameraZ+1), color)
def fix(planets):
    for A in planets:
            if not doMerge:
                for B in planets:
                    if A.id != B.id:
                        d = sqrt( pow( B.x - A.x, 2 )+pow( B.y - A.y, 2 ))
                        if d < A.size + B.size:
                            Av = hypot(A.vx, A.vy)
                            Bv = hypot(B.vx, B.vy)
                            ratioB, ratioB = 0, 0
                            if Av+Bv != 0:
                                ratioB = Av / (Av+Bv)
                                ratioB = Bv / (Av+Bv)
                            excess = A.size + B.size - d
                            angle = atan2(B.y-A.y,B.x-A.x)
                            excessX = cos(angle) * e/2
                            excessY = sin(angle) * e/2
                            A.x -= excessX * ratioB
                            A.y -= excessY * ratioB
                            B.x += excessX * ratioB
                            B.y += excessY * ratioB
            if walls:
                if A.x-A.size <= -wallsX:
                    A.x -= A.x + wallsX - A.size
                if A.y-A.size <= -wallsY:       
                    A.y -= A.y + wallsY - A.size
                if A.x+A.size >= wallsX:
                    A.x -= A.x - wallsX + A.size
                if A.y+A.size >= wallsY:
                    A.y -= A.y - wallsY + A.size
def merge(planets):
    if doMerge:
        for indexA, A in enumerate(planets):
            for indexB, B in enumerate(planets):
                if indexA != indexB:
                    if sqrt( pow( B.x - A.x, 2 )+pow( B.y - A.y, 2 )) < A.size + B.size:
                        ratioA = mass(A) / (mass(A)+mass(B))
                        ratioB = mass(B) / (mass(A)+mass(B))
                        for channel in range(4):
                            A.style[channel] = int(A.style[channel]*ratioA + B.style[channel]*ratioB)
                            A.vx = A.vx*ratioA + B.vx*ratioB
                        A.vy = A.vy*ratioA + B.vy*ratioB
                        A.density = A.density*ratioA + B.density*ratioB
                        A.size = sqrt( pow( A.size, 2) + pow( B.size, 2) )
                        A.x = A.x*ratioA + B.x*ratioB
                        A.x = A.x*ratioA + B.x*ratioB
                        planets.pop(indexB)
                        global followed
                        global orbiter
                        global orbited
                        if indexB == followed:
                            isFolllowing = False
                            followed = indexA
                        if indexB == orbiter:
                            orbiter = indexA
                        if indexB == orbited:
                            orbited = indexA
                        if indexB < followed:
                            followed = followed - 1
                        if indexB < orbiter:
                            orbiter = orbiter - 1
                        if indexB < orbited:
                            orbited = orbited - 1
stars = []
for i in range(1000):
    stars.append([ randint( -width*3, width*6), randint( -height*3, height*6), random()+0.5])

planets = []
for i in range(30):
    planets.append(Planet( randint( -1500, 1500), randint( -1500, 1500), randint( 10, 80), random()*15+15, [ randint( 50, 200), randint( 50, 200), randint( 50, 200), 255]))

template = Planet( 0, 0, 50, 10, [ 0, 80, 180, 255])

set_target_fps(60)

while not window_should_close():
    #simulation
    if playing:
        for A in planets:
            A.update(planets)
            for B in planets:
                if A.id != B.id:
                    d = sqrt( pow( B.x - A.x, 2 )+pow( B.y - A.y, 2 ))
                    if d > A.size + B.size:
                        a = atan2(B.y-A.y,B.x-A.x)
                        force =  G * mass(A) * mass(B) / pow( d, 2)
                        dx = cos(a)*force
                        dy = sin(a)*force
                        A.vx += dx / mass(A)
                        A.vy += dy / mass(A)
        merge(planets)
        fix(planets)
    #input
    dt = get_frame_time()
    if is_key_pressed(KEY_DOWN):
        selected += 1
    if is_key_pressed(KEY_UP):
        selected -= 1
    if is_key_pressed(KEY_SPACE):
        playing = not playing
    if is_key_pressed(KEY_TAB):
        if is_key_down(KEY_LEFT_SHIFT):
            mode -= 1
        else:
            mode += 1
        mode %= 6
    if is_key_down(KEY_KP_ADD):
        power += 1
    if is_key_down(KEY_KP_SUBTRACT):
        power -= 1
    #settings
    if mode == 0:
        selected = selected%6
        if is_key_pressed(KEY_RIGHT)|is_key_pressed(KEY_LEFT):
            if selected == 0:
                walls = not walls
            if selected == 3:
                bounce = not bounce
            if selected == 4:
                doMerge = not doMerge
        if is_key_down(KEY_RIGHT):
            if selected == 1:
                wallsX += power * 10
            if selected == 2:
                wallsY += power * 10
            if selected == 5:
                G += power
        if is_key_down(KEY_LEFT):
            if selected == 1:
                wallsX -= power * 10
            if selected == 2:
                wallsY -= power * 10
            if selected == 5:
                G -= power
    if mode == 1:
        selected = selected%8
        # new planet
        if is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
            drawing = True
            startX = ((get_mouse_x() - width/2)/cameraZ)-cameraX
            startY = ((get_mouse_y() - height/2)/cameraZ)-cameraY
        if is_mouse_button_released(MOUSE_BUTTON_RIGHT):
            drawing = False
            endX = ((get_mouse_x() - width/2)/cameraZ)-cameraX
            endY = ((get_mouse_y() - height/2)/cameraZ)-cameraY
            if not randomize:
                planets.append(Planet( startX, startY, template.size, template.density, template.style))
            else:
                planets.append(Planet( startX, startY, random()*100+10, random()*30+20, [ randint( 50, 200), randint( 50, 200), randint( 50, 200), 255]))
            planets[-1].vx = pow((endX - startX)*cameraZ / 10, 2)
            if endX - startX > 0:
                planets[-1].vx *= -1
            planets[-1].vy = pow((endY - startY)*cameraZ / 10, 2)
            if endY - startY > 0:
                planets[-1].vy *= -1
            planets[-1].static = template.static
        # planet parameters
        if is_key_down(KEY_RIGHT):
            if selected == 0:
                template.size += power
            if selected == 1:
                template.density += power
            if selected == 4:
                if template.style[selected-4] + power <= 255:
                    template.style = [ template.style[0]+power, template.style[1], template.style[2], template.style[3]]
            if selected == 5:
                if template.style[selected-4] + power <= 255:
                    template.style = [ template.style[0], template.style[1]+power, template.style[2], template.style[3]]
            if selected == 6:
                if template.style[selected-4] + power <= 255:
                    template.style = [ template.style[0], template.style[1], template.style[2]+power, template.style[3]]
            if selected == 7:
                if template.style[selected-4] + power <= 255:
                    template.style = [ template.style[0], template.style[1], template.style[2], template.style[3]+power]
        if is_key_down(KEY_LEFT):
            if selected == 0:
                template.size -= power
            if selected == 1:
                template.density -= power
            if selected == 4:
                if template.style[selected-4] - power >= 0:
                    template.style = [ template.style[0]-power, template.style[1], template.style[2], template.style[3]]
            if selected == 5:
                if template.style[selected-4] - power >= 0:
                    template.style = [ template.style[0], template.style[1]-power, template.style[2], template.style[3]]
            if selected == 6:
                if template.style[selected-4] - power >= 0:
                    template.style = [ template.style[0], template.style[1], template.style[2]-power, template.style[3]]
            if selected == 7:
                if template.style[selected-4] - power >= 0:
                    template.style = [ template.style[0], template.style[1], template.style[2], template.style[3]-power]
        if is_key_pressed(KEY_RIGHT)|is_key_pressed(KEY_LEFT):
            if selected == 2:
                template.static = not template.static
            if selected == 3:
                randomize = not randomize
    if mode == 2:
        selected %= 2
        if selected == 0:
            if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
                for i in range(len(planets)):
                    if sqrt( pow(planets[i].x-(((get_mouse_x() - width/2)/cameraZ)-cameraX), 2) + pow(planets[i].y-(((get_mouse_y() - height/2)/cameraZ)-cameraY), 2) ) <= planets[i].size:
                        planets.pop(i)
                        break
        if selected == 1:
            if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
                planets = []
    if mode == 4:
        selected = selected%3
        if selected == 0:
            if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
                for i in range(len(planets)):
                    if sqrt( pow(planets[i].x-(((get_mouse_x() - width/2)/cameraZ)-cameraX), 2) + pow(planets[i].y-(((get_mouse_y() - height/2)/cameraZ)-cameraY), 2) ) <= planets[i].size:
                        orbited = i
                        break
        if selected == 1:
            if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
                for i in range(len(planets)):
                    if sqrt( pow(planets[i].x-(((get_mouse_x() - width/2)/cameraZ)-cameraX), 2) + pow(planets[i].y-(((get_mouse_y() - height/2)/cameraZ)-cameraY), 2) ) <= planets[i].size:
                        orbiter = i
                        break
        if selected == 2:
            if is_key_pressed(KEY_ENTER) or is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
                if orbiter != orbited:
                    A = planets[orbiter]
                    B = planets[orbited]
                    d = sqrt( pow( B.x - A.x, 2 )+pow( B.y - A.y, 2 ))
                    a = atan2(B.y-A.y,B.x-A.x)
                    force =  G * mass(A) * mass(B) / pow( d, 2)
                    print(force)
                    A.vx += cos(a)*force / mass(A)
                    A.vy += sin(a)*force / mass(A)
    if mode == 5:
        selected = selected%2
        if selected == 0:
            if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
                for i in range(len(planets)):
                    if sqrt( pow(planets[i].x-(((get_mouse_x() - width/2)/cameraZ)-cameraX), 2) + pow(planets[i].y-(((get_mouse_y() - height/2)/cameraZ)-cameraY), 2) ) <= planets[i].size:
                        isFolllowing = True
                        followed = i
        if selected == 1:
            if is_key_down(KEY_ENTER) or is_mouse_button_down(MOUSE_BUTTON_RIGHT):
                isFolllowing = False
    #navigation
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
    if isFolllowing:
        cameraX = -planets[followed].x
        cameraY = -planets[followed].y
    #rendering
    begin_drawing()
    clear_background(Color( 3, 3, 5, 255))
    #stars
    for star in stars:
        if cameraZ > 0.01:
            draw_circle( int(star[0]+(cameraX*0.12)), int(star[1]+(cameraY*0.12)), star[2], WHITE)
    for planet in planets:
        planet.draw()
    if walls:
        draw_rectangle_lines( int(( -wallsX+cameraX)*cameraZ + width/2), int(( -wallsY+cameraY)*cameraZ + height/2), int(wallsX*2*cameraZ), int(wallsY*2*cameraZ), WHITE)
    #ui
    if isFolllowing:
            circle_line( planets[followed].x, planets[followed].y, planets[followed].size*1.1, BLUE)
    draw_rectangle( 10, 10, 300, 350, Color( 255, 255, 255, 150))
    draw_rectangle_lines( 10, 10, 300, 350, WHITE)
    for i in range(6):
        draw_rectangle( 320, i*60+10, 150, 50, Color( 255, 255, 255, 180))
        draw_rectangle_lines( 320, i*60+10, 150, 50, WHITE)
        draw_text( modes[i], 325, i*60+18, 34, BLACK)
        if mode == i:
            draw_text( modes[i], 325, i*60+18, 34, selectedColor)
    if mode == 0:
        draw_text( 'mode: settings', 20, 15, 30, BLACK)
        draw_rectangle( 20, 50, 280, 300, Color( 255, 255, 255, 100))
        draw_rectangle_lines( 20, 50, 280, 300, WHITE)
        if selected == 0:
            draw_text_ex( textFont, 'walls: '+str(walls), Vector2( 30, 60), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'walls: '+str(walls), Vector2( 30, 60), 32, 1, BLACK)
        if selected == 1:
            draw_text_ex( textFont, 'walls x: '+str(floor(wallsX/10)), Vector2( 30, 85), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'walls x: '+str(floor(wallsX/10)), Vector2( 30, 85), 32, 1, BLACK)
        if selected == 2:
            draw_text_ex( textFont, 'walls y: '+str(floor(wallsY/10)), Vector2( 30, 110), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'walls y: '+str(floor(wallsY/10)), Vector2( 30, 110), 32, 1, BLACK)
        if selected == 3:
            draw_text_ex( textFont, 'bounce: '+str(bounce), Vector2( 30, 135), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'bounce: '+str(bounce), Vector2( 30, 135), 32, 1, BLACK)
        if selected == 4:
            draw_text_ex( textFont, 'merge: '+str(doMerge), Vector2( 30, 160), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'merge: '+str(doMerge), Vector2( 30, 160), 32, 1, BLACK)
        if selected == 5:
            draw_text_ex( textFont, 'gravity: '+str(G+0.0), Vector2( 30, 185), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'gravity: '+str(G+0.0), Vector2( 30, 185), 32, 1, BLACK)
    if mode == 1:
        draw_text( 'mode: drawing', 20, 15, 30, BLACK)
        draw_rectangle( 20, 50, 280, 300, Color( 255, 255, 255, 100))
        draw_rectangle_lines( 20, 50, 280, 300, WHITE)
        if not randomize:
            draw_circle( 220, 250, template.size/3, template.style)
        else:
            draw_circle( 220, 240, 60, BLACK)
            draw_text( '?', 203, 215, 60, WHITE)
        if selected == 0:
            draw_text_ex( textFont, 'size: '+str(template.size+0.0), Vector2( 30, 60), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'size: '+str(template.size+0.0), Vector2( 30, 60), 32, 1, BLACK)
        if selected == 1:
            draw_text_ex( textFont, 'density: '+str(template.density+0.0), Vector2( 30, 85), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'density: '+str(template.density+0.0), Vector2( 30, 85), 32, 1, BLACK)
        if selected == 2:
            draw_text_ex( textFont, 'static: '+str(template.static), Vector2( 30, 110), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'static: '+str(template.static), Vector2( 30, 110), 32, 1, BLACK)
        if selected == 3:
            draw_text_ex( textFont, 'random: '+str(randomize), Vector2( 30, 135), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'random: '+str(randomize), Vector2( 30, 135), 32, 1, BLACK)
        if selected == 4:
            draw_text_ex( textFont, 'R: '+str(template.style[0]), Vector2( 30, 155), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'R: '+str(template.style[0]), Vector2( 30, 155), 32, 1, BLACK)
        if selected == 5:
            draw_text_ex( textFont, 'G: '+str(template.style[1]), Vector2( 30, 175), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'G: '+str(template.style[1]), Vector2( 30, 175), 32, 1, BLACK)
        if selected == 6:
            draw_text_ex( textFont, 'B: '+str(template.style[2]), Vector2( 30, 200), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'B: '+str(template.style[2]), Vector2( 30, 200), 32, 1, BLACK)
        if selected == 7:
            draw_text_ex( textFont, 'A: '+str(template.style[3]), Vector2( 30, 225), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'A: '+str(template.style[3]), Vector2( 30, 225), 32, 1, BLACK)
    if mode == 2:
        draw_text( 'mode: deleting', 20, 15, 30, BLACK) 
        draw_rectangle( 20, 50, 280, 300, Color( 255, 255, 255, 100))
        if selected == 0:
            draw_text_ex( textFont, 'delete ', Vector2( 30, 60), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'delete ', Vector2( 30, 60), 32, 1, BLACK)
        if selected == 1:
            draw_text_ex( textFont, 'delete all ', Vector2( 30, 85), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, 'delete all ', Vector2( 30, 85), 32, 1, BLACK)
    if mode == 3:
        velocitySum = 0
        massSum = 0
        for planet in planets:
            velocitySum += sqrt(planet.vx**2 + planet.vy**2)
            massSum += mass(planet)
        draw_text( 'mode: statistics', 20, 15, 30, BLACK)
        draw_rectangle( 20, 50, 280, 300, Color( 255, 255, 255, 100))
        draw_text_ex( textFont, 'Planets: '+str(len(planets)), Vector2( 30, 60), 32, 1, BLACK)
        draw_text_ex( textFont, 'velocity: '+str(int(velocitySum/10)), Vector2( 30, 85), 32, 1, BLACK)
        draw_text_ex( textFont, 'mass: '+str(int(massSum)), Vector2( 30, 110), 32, 1, BLACK)
    if mode == 4:
        circle_line( planets[orbiter].x, planets[orbiter].y, planets[orbiter].size*1.1, BLUE)
        circle_line( planets[orbited].x, planets[orbited].y, planets[orbited].size*1.1, GREEN)
        draw_rectangle( 20, 50, 280, 300, Color( 255, 255, 255, 100))
        draw_text( 'mode: make orbit', 20, 15, 30, BLACK)
        if selected == 0:
            draw_text_ex( textFont, '1. select orbited', Vector2( 30, 60), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, '1. select orbited', Vector2( 30, 60), 32, 1, BLACK)
        if selected == 1:
            draw_text_ex( textFont, '2. select orbiter', Vector2( 30, 85), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, '2. select orbiter', Vector2( 30, 85), 32, 1, BLACK)
        if selected == 2:
            draw_text_ex( textFont, '3. make orbit', Vector2( 30, 110), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, '3. make orbit', Vector2( 30, 110), 32, 1, BLACK)
    if mode == 5:
        draw_text( 'mode: camera', 20, 15, 30, BLACK)
        draw_rectangle( 20, 50, 280, 300, Color( 255, 255, 255, 100))
        if selected == 0:
            draw_text_ex( textFont, '1. follow', Vector2( 30, 60), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, '1. follow', Vector2( 30, 60), 32, 1, BLACK)
        if selected == 1:
            draw_text_ex( textFont, '2. release', Vector2( 30, 85), 32, 1, selectedColor)
        else:
            draw_text_ex( textFont, '2. release', Vector2( 30, 85), 32, 1, BLACK)
    if drawing == True:
        line( startX, startY, ((get_mouse_x() - width/2)/cameraZ)-cameraX, ((get_mouse_y() - height/2)/cameraZ)-cameraY, WHITE)
    draw_text( str(power), 270, 17, 30, BLACK)
    if not playing:
        draw_rectangle( width-20, 20, 5, 20, WHITE)
        draw_rectangle( width-31, 20, 5, 20, WHITE)
    end_drawing()
close_window()