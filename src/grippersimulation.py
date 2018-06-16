from vpython import *
import cv2
class Bar: #clase para una barra
    def __init__(self, pbase, pfin, pnormal=vector(1, 0, 0), col=color.cyan):
        self.base = sphere(pos=pbase, radius=0.5, color=color.white)
        self.end = sphere(pos=pfin, radius=0.5, color=color.white)
#       self.norma = sqrt((pbase.x - pfin.x) ** 2 + (pbase.y - pfin.y) ** 2 + (pbase.z - pfin.z) ** 2)
        self.body = cylinder(pos=pbase, radius=0.5, axis=pfin - pbase, color=col)
        self.motor = cylinder(pos=pbase, radius=0.1, axis=pnormal, color=color.white)
        self.atached = []

    def atach(self, bar):
        self.atached.append(bar)

    def check(self):
        bol = True
        if len(self.atached) > 0:
            for elem in self.atached:
                bol = bol and elem.check()
                if(not bol):
                    break
        if(not bol):
            return bol
        return self.base.pos.y>0 and self.end.pos.y>0
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

def to_angles(rot,v180): #funcion para pasar a angulos las vueltas que manda el motor
    # nov ---->  "vueltas" que da el motor para girar 180°
    # rot ---->  "vueltas", lo que manda el motor
    a = (rot*3.141592)/v180
    return a

# medidas en cm
medida_base = 11.6
medida_ele1 = 46.9
medida_ele2 = 4.7
medida_grip = 45.7

#esta es la "mesa"
base = box(pos=vector(0, 0, 0), size=vector(12, 0.2, 12), color=color.white)
#cada parte de los brazos
p = Bar(vector(0, 0, 0), vector(0, medida_base, 0))
p2 = Bar(p.end.pos, vector(0, medida_base, medida_ele1), col=color.blue)
p21 = Bar(p2.end.pos, vector(0, medida_base + medida_ele2, medida_ele1), col=color.blue)
p3 = Bar(p21.end.pos, vector(0, medida_base + medida_ele2, medida_ele1 - medida_grip), col=color.yellow)
p.atach(p2)
p2.atach(p21)
p21.atach(p3)





# numero de vueltas que marca cada motor para girar 180° /////////////////////////////////////////////
# (no puede ser 0)
vueltas_para_180_motor1 = 100
vueltas_para_180_motor2 = 100
vueltas_para_180_motor3 = 100



# montar conexion y recibir datos //////////////////////////////////

motor1 = 0  # motor que gira el brazo en la base
motor2 = 0  # motor que mueve el primer segmento
motor3 = 0  # motor que mueve el segundo segmento

# valor anterior de cada motor
motor1_anterior = 0
motor2_anterior = 0
motor3_anterior = 0

while True:

    # hay que leer datos////////////////////////////////////////////

    if(True): #debe ser: if(se reciben los siguientes datos):///////////////////////////////////////

        #Aqui actualiza los valores de "vueltas" que mande cada motora////////////////////////////////////
        valor1 = 0 #/////
        valor2 = 0 #/////
        valor3 = 0 #/////


        motor1 = valor1 - motor1_anterior
        motor2 = valor2 - motor2_anterior
        motor3 = valor3 - motor3_anterior

        p.rotate(to_angles(motor1,vueltas_para_180_motor1))
        p2.rotatem(to_angles(motor2, vueltas_para_180_motor2))
        if(not p2.check()):
            p2.rotatem(to_angles(-motor2, vueltas_para_180_motor2))
        p3.rotatem(to_angles(motor3, vueltas_para_180_motor3))
        if(p3.check()):
            p3.rotatem(to_angles(-motor3,vueltas_para_180_motor3))

        motor1_anterior = valor1
        motor2_anterior = valor2
        motor3_anterior = valor3
