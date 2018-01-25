from struct import *

UDP_IP = "192.168.1.9"
UDP_PORT = 5000


def to_m(v):
    if v > 0:
        return int(abs(v) * 1000)
    if v < 0:
        return int(abs(v) * 999 + 1001)
    if v == 0:
        return int(2)  # falta ver aqui que valor mandar


def st(x, y):
    ny = abs(y) - abs(x * y)
    a = abs(ny) + abs(x)
    b = abs(y) - abs(x)
    if y < 0:
        a = -a  # espejeamos la funcion
        b = -b
        n = b
        b = a
        a = n
    if x < 0:
        return (b, a)
    else:
        return (a, b)


def send_data(self, i, v):
    data = pack('BBBBBB', 0, i, 1, int(v / 254 + 1), int(v % 254 + 1), 255)
    try:
        self.sock.sendto(data, (UDP_IP, UDP_PORT))
        s = unpack('BBBBBB', data)
        self.statusbar.showMessage(str(s), 5000)
    except:
        self.statusbar.showMessage("Error sending data", 5000)


def move_robot(m1, m2):
    print(m1)
    print(m2)
    send_data(2, to_m(m1))
    send_data(4, to_m(m2))
