from vpython import *

# ball = sphere(pos=vector(0,0,0), radius=0.5, color=color.cyan)
base = box(pos=vector(0, 0, 0), size=vector(12, 0.2, 12), color=color.white)

# medidas en cm
mbase = 11.6
mele1 = 46.9
mele2 = 4.7
mbrazo = 45.7


class Barra:
    def __init__(self, pbase, pfin, pnormal=vector(1, 0, 0), col=color.cyan):
        self.base = sphere(pos=pbase, radius=0.5, color=color.white)
        self.fin = sphere(pos=pfin, radius=0.5, color=color.white)
#       self.norma = sqrt((pbase.x - pfin.x) ** 2 + (pbase.y - pfin.y) ** 2 + (pbase.z - pfin.z) ** 2)
        self.body = cylinder(pos=pbase, radius=0.5, axis=pfin - pbase, color=col)
        self.motor = cylinder(pos=pbase, radius=0.1, axis=pnormal, color=color.white)
        self.atached = []

    def atach(self, barra):
        self.atached.append(barra)

    def rotate(self, angle):
        self.fin.rotate(angle, self.fin.pos - self.base.pos, self.base.pos)
        self.body.rotate(angle, self.fin.pos - self.base.pos, self.base.pos)
        self.motor.rotate(angle, self.fin.pos - self.base.pos, self.base.pos)
        if len(self.atached) > 0:
            for elem in self.atached:
                elem.__rotate(angle, self.fin.pos - self.base.pos, self.base.pos)

    def rotatem(self, angle):
        self.fin.rotate(angle, self.motor.axis, self.base.pos)
        self.body.rotate(angle, self.motor.axis, self.base.pos)
        if len(self.atached) > 0:
            for elem in self.atached:
                elem.__rotate(angle, self.motor.axis, self.base.pos)

    def __rotate(self, angle, axis, origin):
        self.fin.rotate(angle, axis, origin)
        self.base.rotate(angle, axis, origin)
        self.body.rotate(angle, axis, origin)
        self.motor.rotate(angle, axis, origin)
        if len(self.atached) > 0:
            for elem in self.atached:
                elem.__rotate(angle, axis, origin)


p = Barra(vector(0, 0, 0), vector(0, mbase, 0))
p2 = Barra(p.fin.pos, vector(0, mbase, mele1), col=color.blue)
p21 = Barra(p2.fin.pos, vector(0, mbase + mele2, mele1), col=color.blue)
p3 = Barra(p21.fin.pos, vector(0, mbase + mele2, mele1 - mbrazo), col=color.yellow)
p.atach(p2)
p2.atach(p21)
p21.atach(p3)

while True:
    p.rotate(0.001)
