#! /usr/bin/python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Wed Jun  1 23:08:27 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import cv2
import socket
import xbox
import time
import vlc
import serial
import sys
from struct import *

#Control de xbox conectar
joy = xbox.Joystick()

#Configuracion de IP para entrar al robot
UDP_IP = "192.168.1.9"
RUDP_IP = "127.0.0.1"
RUDP_PORT = 5001
UDP_PORT = 5000
MESSAGE = "HI"

datos = ""

#Cosas raras de interfaz gráfica de Qt que no debemos de entender
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


#Funcion que se utiliza para procesar valores de los joystick y que el robot los pueda procesar
def toM(v):
    if v > 0:
        return int(abs(v) * 1000)
    if v < 0:
        return int(abs(v) * 999 + 1001)
    if v == 0:
        return int(2)

#Funcion que se utiliza para procesar valores de los botones y que el robot los pueda procesar
def Bt(a, b, z):
    if a and not b:
        return int(1000 / z)
    elif b:
        return int((1001 + (1000 / z)))
    else:
        return int(2)  # falta ver aqui que valor mandar

#Funcion auxiliar para cambiar los valores a como los queremos
def St(x, y):
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
        return (b, a)
    else:
        return (a, b)


#Funcion de Interfaz Grafica para cerrar ventana
class MyWindow(QtGui.QMainWindow):
    def closeEvent(self, event):
        joy.close()
        event.accept()

#Funcion para poner lo que necesitamos en la interfaz grafica (incluido las camaras)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1200, 675)

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        self.mediaplayer2 = self.instance.media_player_new()
        self.mediaplayer3 = self.instance.media_player_new()
        self.mediaplayer4 = self.instance.media_player_new()

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(1030, 10, 134, 62))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.verticalLayoutWidget)
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.joystick_clicked)
        self.gridLayout_2.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), self.wiznet_clicked)
        self.gridLayout_2.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 10, 1011, 611))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.CamView2 = QtGui.QFrame(self.gridLayoutWidget)
        self.CamView2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.CamView2.setObjectName(_fromUtf8("CamView2"))
        self.gridLayout.addWidget(self.CamView2, 0, 1, 1, 1)
        self.CamView3 = QtGui.QFrame(self.gridLayoutWidget)
        self.CamView3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.CamView3.setObjectName(_fromUtf8("CamView3"))
        self.gridLayout.addWidget(self.CamView3, 1, 0, 1, 1)
        self.CamView = QtGui.QFrame(self.gridLayoutWidget)
        self.CamView.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.CamView.setObjectName(_fromUtf8("CamView"))
        self.gridLayout.addWidget(self.CamView, 0, 0, 1, 1)
        self.CamView4 = QtGui.QFrame(self.gridLayoutWidget)
        self.CamView4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.CamView4.setObjectName(_fromUtf8("CamView4"))
        self.gridLayout.addWidget(self.CamView4, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.timerC = QtCore.QTimer()  # Inicializacion del timer
        self.timerC.setSingleShot(False)
        self.timerC.timeout.connect(self.camerat)
        self.timerC.start(100)
        self.timerD = QtCore.QTimer()  # Inicializacion del timer
        self.timerD.setSingleShot(False)
        self.timerD.timeout.connect(self.form_t)
        self.sensor = ""
        self.timerD.start(10)
        self.timerJ = QtCore.QTimer()  # Inicializacion del timer
        self.timerJ.setSingleShot(False)
        self.timerJ.timeout.connect(self.joyupdate_t)
        self.joyv = 0
        # ser.open()
        # self.timerJ.start(10)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.camera1 = 0
        self.camera2 = 0
        self.camera3 = 0
        self.camera4 = 0
        self.updatec = 1
        self.updatem = 1
        self.mode = 0
        self.initsensor = 0
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #Conexion a el robot
    def form_t(self):
        if self.initsensor == 0:
            try:
                # self.sock1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                server_address = ("192.168.1.5", 5000)
            # self.sock1.bind(server_address)
            # self.initsensor = 1
            except:
                self.statusbar.showMessage("Error sensor", 5000)
        else:
            try:
                data, add = self.sock1.recvfrom(1024)
                wiza = ('192.168.1.9', 5000)
                if wiza == add:
                    temp = str(data)
                    if temp.find("!") == -1:
                        self.datos = str(self.datos) + str(temp)
                        if temp.find("\n") == -1:
                            self.datos = self.datos
                        else:
                            self.sensor = self.datos
                            print
                            self.datos
                    else:
                        self.datos = str(temp)
            except:
                self.statusbar.showMessage("Error sensor", 5000)
        if self.sensor != "":
            cos = ""
            for s in range(1, 4):
                if self.sensor[s].isdigit():
                    cos = cos + self.sensor[s]
            cos = int(cos)
            t = ""
            for s in range(10, 15):
                if self.sensor[s].isdigit() or self.sensor[s] == ".":
                    t = t + self.sensor[s]
            t = float(t)
            cos = abs(cos - 110) * 100
            self.pushButton.setText(_translate("MainWindow", "CO2:" + str(cos) + " " + "Temp:" + str(t), None))
        x = MainWindow.frameGeometry().width()
        y = MainWindow.frameGeometry().height()
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 10, x - 170, y - 80))
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(x - 160, 10, 134, 62))

#Esta funcion es importante, es la que se encarga de mandar datos al robot, se utiliza para mandar comandos de las llantas
#mas adelante esta mejor detallada.
    def sendC(self, i, v):
        BYTES = pack('BBBBBB', 0, i, 1, int(v / 254 + 1), int(v % 254 + 1), 255)
        try:
            self.sock.sendto(BYTES, (UDP_IP, UDP_PORT))
            # ser.write(BYTES)
            s = unpack('BBBBBB', BYTES)
            self.statusbar.showMessage(str(s), 5000)
        except:
            self.statusbar.showMessage("Error sending data", 5000)

#Esta funcion es para prender las camaras y recibir los datos de ellas
    def camerat(self):
        if joy.leftThumbstick():
            if self.updatec == 0:
                self.camera1 = 0
                self.camera2 = 0
                self.camera3 = 0
                self.camera4 = 0
                self.updatec = 1
            if joy.A(): self.camera1 = 1
            if joy.B(): self.camera2 = 1
            if joy.X(): self.camera3 = 1
            if joy.Y(): self.camera4 = 1
        else:
            if self.updatec == 1:
                self.updatec = 0
                if self.camera1 == 1 or self.camera2 == 1 or self.camera3 == 1 or self.camera4 == 1:
                    self.CamView2.hide()
                    self.CamView3.hide()
                    self.CamView4.hide()
                    if self.camera1 == 1: filename = "rtsp://192.168.1.11/live3.sdp"
                    if self.camera2 == 1: filename = "rtsp://192.168.1.15/user=admin_password=tlJwpbo6_channel=1_stream=1.sdp"
                    if self.camera3 == 1: filename = "rtsp://192.168.1.13/live3.sdp"
                    if self.camera4 == 1: filename = "rtsp://192.168.1.14/live3.sdp"
                    self.media = self.instance.media_new(filename)
                    self.media.add_options("network-caching=95")
                    self.mediaplayer.set_media(self.media)
                    self.media.parse()
                    self.mediaplayer.play()
                    self.mediaplayer.set_xwindow(self.CamView.winId())

                if self.camera1 == 0 and self.camera2 == 0 and self.camera3 == 0 and self.camera4 == 0:
                    self.CamView2.show()
                    self.CamView3.show()
                    self.CamView4.show()
                    filename = "rtsp://192.168.1.11/live2.sdp"
                    self.media = self.instance.media_new(filename)
                    self.media.add_options("network-caching=90")
                    self.mediaplayer.set_media(self.media)
                    self.media.parse()
                    self.mediaplayer.play()
                    self.mediaplayer.set_xwindow(self.CamView.winId())
                    filename = "rtsp://192.168.1.15/user=admin_password=tlJwpbo6_channel=1_stream=0.sdp"
                    self.media2 = self.instance.media_new(filename)
                    self.media2.add_options("network-caching=90")
                    self.mediaplayer2.set_media(self.media2)
                    self.media2.parse()
                    self.mediaplayer2.play()
                    self.mediaplayer2.set_xwindow(self.CamView2.winId())
                    filename = "rtsp://192.168.1.13/live2.sdp"
                    self.media3 = self.instance.media_new(filename)
                    self.media3.add_options("network-caching=90")
                    self.mediaplayer3.set_media(self.media3)
                    self.media3.parse()
                    self.mediaplayer3.play()
                    self.mediaplayer3.set_xwindow(self.CamView3.winId())
                    filename = "rtsp://192.168.1.16/live2.sdp"
                    self.media4 = self.instance.media_new(filename)
                    self.media4.add_options("network-caching=90")
                    self.mediaplayer4.set_media(self.media4)
                    self.media4.parse()
                    self.mediaplayer4.play()
                    self.mediaplayer4.set_xwindow(self.CamView4.winId())

#Funcion necesaria de QT para refrescar las ventanas
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "Conectar control", None))
        self.pushButton_2.setText(_translate("MainWindow", "Manipulacion", None))

    # self.statusbar.showMessage("Conectando",5000)

#Funcion para ver si el control de xbox esta conectado
    def joystick_clicked(self):
        if self.joyv == 0:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.datos = ""
            self.joyv = 1
            self.timerJ.start(40)
            self.statusbar.showMessage("Control conectado", 1000)
        else:
            if self.joyv == 1:
                self.joyv = 0
                self.timerJ.stop()
                self.statusbar.showMessage("Control desconectado", 1000)

    def wiznet_clicked(self):
        if self.joyv == 0:
            self.joyv = 1
            self.timerJ.start(40)
            self.statusbar.showMessage("Control conectado", 1000)
        else:
            if self.joyv == 1:
                self.joyv = 0
                self.timerJ.stop()
                self.statusbar.showMessage("Control desconectado", 1000)

#Funcion que detecta si el control se desconecto, si es asi se para el robot e imprime 'corran'
    def joyupdate_t(self):
        try:
            # Valid connect may require joystick input to occur
            if not joy.connected():
                self.statusbar.showMessage("Error joy", 5000)
        except:
            print ("corran")

        # Show misc inputs until Back button is pressed    Bt(joy.rightBumper(),joy.leftBumper())  Bt(joy.Y(),joy.A())
        if joy.connected():  # tr1, 			tr2, 		fl1 ,		fl2 ,			gripper, 			muñeca, 					girogrip, 		extension, girobrazo, Act1, Act2
            if joy.Back() and self.updatem == 1:
                self.updatem = 0
                if self.mode == 1:
                    self.mode = 0
                    self.pushButton_2.setText(_translate("MainWindow", "Manipulacion", None))
                else:
                    self.mode = 1
                    self.pushButton_2.setText(_translate("MainWindow", "Movilidad", None))
            elif not joy.Back() and self.updatem == 0:
                self.updatem = 1

            (m1, m2) = St(joy.leftX(), joy.leftY())
            if self.mode == 1:
                self.sendC(2, toM(joy.leftY()))
                self.sendC(4, toM(joy.rightY()))
                self.sendC(1, toM(joy.leftX()))
                self.sendC(3, toM(joy.rightX()))

            else:
                self.sendC(2, toM(m1))
                self.sendC(4, toM(m2))
                self.sendC(1, 1)
                self.sendC(2, 1)
                self.sendC(8, toM(joy.rightX()))
                self.sendC(9, toM(joy.rightY()))
                self.sendC(7, Bt(joy.rightBumper(), joy.leftBumper(), 1))
                self.sendC(6, Bt(joy.Y(), joy.A(), 1))
                self.sendC(5, toM(joy.rightTrigger() - joy.leftTrigger()))
                self.sendC(10, Bt(joy.dpadDown(), joy.dpadUp(), 1.2))
                self.sendC(11, Bt(joy.dpadLeft(), joy.dpadRight(), 1.2))

''' Las siguientes lineas de codigo son las mas improtantes del robot, se encargan de mandar los datos del joystick a
el robot mediante la funcion sendC, a continuacion documento que es lo que hace cada boton del joystick. El roboto tiene
2 modos: manipulacion y normal, en manipulacion hace enfasis en la posicion de las llantas, mientras que el normal es
con el que se meuve el brazo y controles basicos del robot.
'''
'''
Normal:
Joystick derecho: Mover adelante, atrás, izquierda y derecha.
Joystick izquierdo: Mover mano, adelante, atrás y girar.
D- Pad: Mover todo el brazo adelante / atrás.
Y: Hacer brazo más chico. PENDIENTE PRUEBA
A: Hacer brazo más grande. PENDIENTE PRUEBA
LB, RB: Abrir y cerrar brazo. PENDIENTE PRUEBA
LT, RT: Mover brazo izquierda, derecha. PENDIENTE PRUEBA

Manipulación: 
Joystick izquierdo, izquierda: Subir Llantas traseras. St, ToM
Joystick izquierdo, derecha: Bajar Llantas traseras.
Joystick izquierdo, adelante / atrás: mover llantas izquierdas.
Joystick derecho, izquierda: Subir Llantas delanteras.
Joystick derecho, derecha: Bajar Llantas delanteras.
Joystick derecho, adelante / atrás: mover llantas derechas.
'''

#aqui se corre todo
if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    MainWindow = MyWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

