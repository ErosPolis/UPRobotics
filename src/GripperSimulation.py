from vpython import *

# ball = sphere(pos=vector(0,0,0), radius=0.5, color=color.cyan)
base = box(pos=vector(0, 0, 0), size=vector(12, 0.2, 12), color=color.white)

# medidas en cm
mbase = 11.6
mele1 = 46.9
mele2 = 4.7
mbrazo = 45.7


class Barra:
    def __init__(self, pbase, pfin, col=color.cyan):
        self.base = sphere(pos=pbase, radius=0.5, color=color.white)
        self.fin = sphere(pos=pfin, radius=0.5, color=color.white)
        self.norma = sqrt((pbase.x - pfin.x) ** 2 + (pbase.y - pfin.y) ** 2 + (pbase.z - pfin.z) ** 2)
        self.body = cylinder(pos=pbase, radius=0.5, axis=pfin - pbase, color=col)
        self.atached = []

    def atach(self, barra):
        self.atached.append(barra)

    def rotate(self, angle):
        self.fin.rotate(angle, self.fin.pos - self.base.pos, self.base.pos)
        self.body.rotate(angle, self.fin.pos - self.base.pos, self.base.pos)
        if (len(self.atached) > 0):
            for x in self.atached:
                x.rotateb(angle, self.fin.pos - self.base.pos, self.base.pos)

    def rotatel(self, angle):
        self.fin.rotate(angle, self.fin.pos - self.base.pos, self.base.pos)
        self.body.rotate(angle, self.fin.pos - self.base.pos, self.base.pos)
        if (len(self.atached) > 0):
            for x in self.atached:
                x.rotateb(angle, self.fin.pos - self.base.pos, self.base.pos)

    def rotateb(self, angle, axis, origin):
        self.fin.rotate(angle, axis, origin)
        self.base.rotate(angle, axis, origin)
        self.body.rotate(angle, axis, origin)
        if (len(self.atached) > 0):
            for x in self.atached:
                x.rotateb(angle, axis, origin)


x = Barra(vector(0, 0, 0), vector(0, mbase, 0))
x2 = Barra(x.fin.pos, vector(0, mbase, mele1))
x3 = Barra(x2.fin.pos, vector(0, mbase + mele2, mele1))
xx1 = Barra(x3.fin.pos, vector(0, mbase + mele2, mele1 - mbrazo))
x.atach(x2)
x2.atach(x3)
x3.atach(xx1)

while True:
    x.rotate(0.001)
    x2.rotate(0.001)
