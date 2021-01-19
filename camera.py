from OpenGL.GL import *
import math

class FPS:
    def __init__(self):
        self.pos = [0,0,0]
        self.elev = 0
        self.rot = 0

    def load_matrix(self):
        glRotatef(-self.elev, 1, 0, 0)
        glRotatef(self.rot, 0, 1, 0)
        glTranslatef(-self.pos[0], -self.pos[1], -self.pos[2])

    def walk(self, dist):
        x = math.sin(self.rot * math.pi / 180.0) * dist
        z = math.cos(self.rot * math.pi / 180.0) * dist

        self.pos[0] += x
        self.pos[2] -= z


class Trackball:
    def __init__(self):
        self.pos = [0,0,0]
        self.elev = 0
        self.rot = 0
        self.dist = 0

    def load_matrix(self):
        glTranslatef(0, 0, -self.dist)
        glRotatef(-self.elev, 1, 0, 0)
        glRotatef(self.rot, 0, 1, 0)
        glTranslatef(-self.pos[0], -self.pos[1], -self.pos[2])
        