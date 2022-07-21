#Programa para crear una ventana de Graficos que se represente a través de un mapa de bits
#El programa fue creado con la ayuda del catedrático Carlos Alonso y es casi una copia de lo hecho en clase



import struct
from collections import namedtuple
import random

V2 = namedtuple('Point2', ['x', 'y'])

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r,g,b):
    return bytes([int(b*255),int(g*255),int(r*255)])


class Renderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clearColor = color(0, 0, 0)
        self.currColor = color(1, 1, 1)
        
        self.glClear()
        self.glViewPort(0, 0, self.width, self.height)
        
    def glClear(self):
        self.pixels = [[self.clearColor for y in range(self.height)] for x in range(self.width)]
        
    def glClearColor(self, r, g, b):
        self.clearColor = color(r, g, b)
        
    def glColor(self, r, g, b):
        self.currColor = color(r, g, b)
        
    def glPoint(self, x, y, clr = None):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor
            
    def glViewPort(self, posX, posY, width, height):
        self.vpx = posX
        self.vpy = posY
        self.vpwidth = width
        self.vpheight = height
        
    def glClearViewport(self, clr = None):
        for x in range(self.vpx, self.vpx + self.vpwidth):
            for y in range(self.vpy, self.vpy + self.vpheight):
                self.glPoint(x,y,clr)
                
    def glPoint_vp(self, ndcX, ndcY, clr = None):
        if ndcX < -1 or ndcX > 1 or ndcY < -1 or ndcY > 1:
            return

        x = (ndcX + 1) * (self.vpwidth / 2) + self.vpx
        y = (ndcY + 1) * (self.vpheight / 2) + self.vpy

        x = int(x)
        y = int(y)
        
        self.glPoint(x,y,clr)
    
    
    def glLine(self, v0, v1, clr = None):
            # Bresenham line algorithm
        # y = m * x + b
        x0 = int(v0.x)
        x1 = int(v1.x)
        y0 = int(v0.y)
        y1 = int(v1.y)

        # Si el punto0 es igual al punto 1, dibujar solamente un punto
        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y0,clr)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        # Si la linea tiene pendiente mayor a 1 o menor a -1
        # intercambio las x por las y, y se dibuja la linea
        # de manera vertical
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Si el punto inicial X es mayor que el punto final X,
        # intercambio los puntos para siempre dibujar de 
        # izquierda a derecha       
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.5
        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                # Dibujar de manera vertical
                self.glPoint(y, x, clr)
            else:
                # Dibujar de manera horizontal
                self.glPoint(x, y, clr)

            offset += m

            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                
                limit += 1

    #Ayuda obtenida de https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule#:~:text=If%20this%20number%20is%20odd,to%20fill%20in%20strange%20ways. Utililzando la even odd rule para saber si un punto es boundary o no
    def boundaries(self, x: int, y: int, poly) -> bool:
        num = len(poly)
        j = num - 1
        c = False
        for i in range(num):
            if (x == poly[i][0]) and (y == poly[i][1]):
                #El punto que se esta viendo es una esquina
                return True
            
            #El punto que se esta biendo está dentro de la figura tomando en cuenta la pendiente de  los puntos
            if ((poly[i][1] > y) != (poly[j][1] > y)):
                slope = (x-poly[i][0])*(poly[j][1]-poly[i][1])-(poly[j][0]-poly[i][0])*(y-poly[i][1])
                if slope == 0:
                    return True
                #REvisa si el slope es una linea horizontal y por lo tanto seria considerado un boundary
                if (slope < 0) != (poly[j][1] < poly[i][1]):
                    #Revisa si el punto que se está viendo está dentro de la figura
                    c = not c
            j = i
        return c
    
    def glFill(self,poly,color = None):
        for i in range(self.height):
            for j in range(self.width):
                if  self.boundaries(i,j,poly):
                    self.glPoint(i,j, clr = color)
                    
    def randomGlFill(self,poly,color=None):
        for i in range(self.height):
            for j in range(self.width):
                if self.boundaries(i,j,poly):
                    self.glPoint(i,j, clr = (random.Random(),random.Random(),random.Random()))
                
        
        
        
    def glFinish(self, filename):
        with open(filename, "wb") as file:
            #header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(14 + 40))
            
            
            #info header
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            
            
            #Color Tables
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
                    
            