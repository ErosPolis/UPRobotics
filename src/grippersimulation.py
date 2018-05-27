from vpython import *

base = box(pos=vector(0, 0, 0), size=vector(12, 0.2, 12), color=color.white)


mbase = 11.6
mele1 = 46.9
mele2 = 4.7
mgrip = 45.7


class Bar:
    def __init__(self, pbase, pfin, pnormal=vector(1, 0, 0), col=color.cyan):
        self.base = sphere(pos=pbase, radius=0.5, color=color.white)
        self.end = sphere(pos=pfin, radius=0.5, color=color.white)
        self.body = cylinder(pos=pbase, radius=0.5, axis=pfin - pbase, color=col)
        self.motor = cylinder(pos=pbase, radius=0.1, axis=pnormal, color=color.white)
        self.atached = []

    def attach(self, bar):
        self.atached.append(bar)

    def rotate(self, angle):
        self.end.rotate(angle, self.end.pos - self.base.pos, self.base.pos)
        self.body.rotate(angle, self.end.pos - self.base.pos, self.base.pos)
        self.motor.rotate(angle, self.end.pos - self.base.pos, self.base.pos)
        if len(self.atached) > 0:
            for elem in self.atached:
                elem.__rotate(angle, self.end.pos - self.base.pos, self.base.pos)

    def rotatem(self, angle):
        self.end.rotate(angle, self.motor.axis, self.base.pos)
        self.body.rotate(angle, self.motor.axis, self.base.pos)
        if len(self.atached) > 0:
            for elem in self.atached:
                elem.__rotate(angle, self.motor.axis, self.base.pos)

    def __rotate(self, angle, axis, origin):
        self.end.rotate(angle, axis, origin)
        self.base.rotate(angle, axis, origin)
        self.body.rotate(angle, axis, origin)
        self.motor.rotate(angle, axis, origin)
        if len(self.atached) > 0:
            for elem in self.atached:
                elem.__rotate(angle, axis, origin)


p = Bar(vector(0, 0, 0), vector(0, mbase, 0))
p2 = Bar(p.end.pos, vector(0, mbase, mele1), col=color.blue)
p21 = Bar(p2.end.pos, vector(0, mbase + mele2, mele1), col=color.blue)
p3 = Bar(p21.end.pos, vector(0, mbase + mele2, mele1 - mgrip), col=color.yellow)
p.attach(p2)
p2.attach(p21)
p21.attach(p3)

while True:
    p.rotate(0.001)
