#Programa para crear una ventana de Graficos que se represente a través de un mapa de bits
#El programa fue creado con la ayuda del catedrático Carlos Alonso y es casi una copia de lo hecho en clase

from gl import Renderer, color, V2
import random

width = 1920
height = 1080

rend = Renderer(width, height)
rend.glColor(1, 1, 1)
''' steps = 100

dy = height / steps
dx = width / steps

x = 0
y = height
for i in range(steps):
    rend.glLine(V2(x,0), V2(0, y))
    rend.glLine(V2(x,0), V2(width, height - y))
    rend.glLine(V2(width - x,height), V2(0, y))
    rend.glLine(V2(width - x,height), V2(width, height - y))
    x += dx
    y -= dy
 '''
p1 = [V2(300, 300), V2(400, 300), V2(300, 400)]
p2 = [V2(500,300), V2(600,300), V2(600, 400), V2(500, 400)]
p3 = [V2(700,300), V2(800,300), V2(800, 400), V2(750, 500), V2(700, 400)]
p4 = [V2(900,300), V2(1000,300), V2(1000, 400), V2(950, 350), V2(900, 400)]
p5 = [V2(1150,300), V2(1200, 400), V2(1150, 350), V2(1100, 400)]

for i in range(len(p1)):
    rend.glLine(p1[i], p1[(i + 1) % len(p1)])
    
for i in range(len(p2)):
    rend.glLine(p2[i], p2[(i + 1) % len(p2)])
    
for i in range(len(p3)):
    rend.glLine(p3[i], p3[(i + 1) % len(p3)])
    
for i in range(len(p4)):
    rend.glLine(p4[i], p4[(i + 1) % len(p4)])

for i in range(len(p5)):
    rend.glLine(p5[i], p5[(i + 1) % len(p5)])
''' #Poligono 1
poligono1 = [V2(165, 380), V2(185, 360),V2(180, 330),V2(207, 345), V2(233, 330), V2(230, 360), V2(250, 380), V2(220, 385), V2(205, 410), V2(193, 383)]
poligono1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]

poligono2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
poligono3 = [(377, 249), (411, 197), (436, 249)]
poligono4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
            (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
            (597, 215), (552, 214), (517, 144), (466, 180)]

poligono5 = [(682, 175), (708, 120), (735, 148), (739, 170)]

figuras = [poligono1, poligono2, poligono3, poligono4, poligono5]


for i in figuras:
    rend.glFill(i, color(random.random(), random.random(), random.random()))
    if i == poligono5:
        rend.glFill(i, color(0, 0, 0))
 '''



rend.glFinish("test.bmp")