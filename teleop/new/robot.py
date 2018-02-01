from struct import *


class Robot():
    def __init__(self, ip = "192.168.1.9", port = 5000):
        self.UDP_IP = ip
        self.UDP_PORT = port

    # Move the whole robot, front, back, left and right.
    def move_robot(self, value_x, value_y):
        self.send_data(2, value_x)
        self.send_data(1, value_y)

    # Move the hand, up, down and rotate.
    def move_hand(self, value_x, value_y):
        self.send_data(8, value_x)
        self.send_data(9, value_y)

    # Move the whole arm, left and right.
    def move_arm_x(self, value):
        self.send_data(7, value)

    # Move the arm size.
    def move_arm_size(self, value):
        self.send_data(6, value)

    # Move whole arm, up and down.
    def move_arm_y(self, value):
        self.send_data(value)

    # When you don't use the motors, you must shut them down, when you send 1, it automatically shuts down.
    def shutdown_motors(self, motors):
        for motor in motors:
            self.send_data(motor, 1)

    # Send bytes to robot.
    def send_data(self, i, v):
        data = pack('BBBBBB', 0, i, 1, int(v / 254 + 1), int(v % 254 + 1), 255)
        try:
            self.sock.sendto(data, (self.UDP_IP, self.UDP_PORT))
            s = unpack('BBBBBB', data)
            self.statusbar.showMessage(str(s), 5000)
        except:
            self.statusbar.showMessage("Error sending data", 5000)

    @staticmethod
    def to_m(v):
        if v > 0:
            return int(abs(v) * 1000)
        if v < 0:
            return int(abs(v) * 999 + 1001)
        if v == 0:
            return int(2)

    @staticmethod
    def button(a, b, z):
        if a and not b:
            return int(1000 / z)
        elif b:
            return int((1001 + (1000 / z)))
        else:
            return int(2)

    @staticmethod
    def st(self, x, y):
        ny = abs(y) - abs(x * y)
        a = abs(ny) + abs(x)
        b = abs(y) - abs(x)
        if y < 0:
            a = -a
            b = -b
            n = b
            b = a
            a = n
        if x < 0:
            return b, a
        else:
            return a, b


