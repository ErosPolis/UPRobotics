import socket
from struct import *

UDP_IP = "192.168.1.5"
UDP_PORT = 5001
TUDP_IP = "192.168.1.9"
TUDP_PORT = 5000

def send_data(i):
    data = pack('BBBB', 0, i, 1, 255)
    try:
        sock2.sendto(data, (TUDP_IP, TUDP_PORT))
        s = unpack('BBBB', data)
        print(s)
    except:
        print("Error sending data")

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock2 = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

data = []
while 1:
	try:
		#send_data(6)
		b = sock.recvfrom(1)
		#print(b)
		s = unpack('B',b[0:1])
		print(s)
		if s[0] == 0:
			data.append(s)
			while s[0] != 255:
				b = sock.recvfrom(1)
				print(b)
				s = unpack('B',b[0:1])
				print(s)
				data.append(s)
				print("llenando")
			print(data)
	except Exception as e:
		raise e
		print("no")
	data = []
    