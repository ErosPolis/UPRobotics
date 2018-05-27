import socket
import pyaudio


class AudioSender:
    def __init__(self, host='192.168.1.128', port=50007, rate=44100, channels=1, format_type=pyaudio.paInt16,
                 chunk=1024):
        self.rate = rate
        self.channels = channels
        self.format_type = format_type
        self.chunk = chunk
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.p = pyaudio.PyAudio()

    def send_data(self, record_seconds=5):
        stream = self.p.open(format=self.format_type,
                             channels=self.channels,
                             rate=self.rate,
                             input=True,
                             frames_per_buffer=self.chunk)

        print("recording audio")

        frames = []

        for i in range(0, int(self.rate / self.chunk * record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
            self.s.sendall(data)

        print("*done recording")

        stream.stop_stream()
        stream.close()
        self.p.terminate()
        self.s.close()

        print("*closed")


conn = AudioSender()
conn.send_data()
