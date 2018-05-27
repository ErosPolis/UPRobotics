import socket
import pyaudio
import wave


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

        print("Recording audio...")

        frames = []

        for i in range(0, int(self.rate / self.chunk * record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
            self.s.sendall(data)

        print("Done recording, playing audio")

        stream.stop_stream()
        stream.close()
        self.p.terminate()
        self.s.close()

        print("Closed.")


class AudioReceiver:
    def __init__(self, host='', port=50007, rate=44100, channels=1, format_type=pyaudio.paInt16,
                 chunk=1024, width=2):
        self.rate = rate
        self.channels = channels
        self.format_type = format_type
        self.chunk = chunk
        self.width = width
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))

    def listen(self, filename="/home/pi/server_output.wav"):
        audio_stream = self.p.open(format=self.p.get_format_from_width(self.width),
                                   channels=self.channels,
                                   rate=self.rate,
                                   output=True,
                                   frames_per_buffer=self.chunk)

        self.s.listen(1)
        connection, ip_address = self.s.accept()
        print('Connected by', ip_address)
        audio_data = connection.recv(1024)

        frame = 1
        while audio_data != '':
            audio_stream.write(audio_data)
            audio_data = connection.recv(1024)
            frame = frame + 1
            print("Frame " + str(frame) + " received")
            self.frames.append(audio_data)

        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(self.p.get_sample_size(self.format_type))
        wave_file.setframerate(self.rate)
        wave_file.writeframes(b''.join(self.frames))
        wave_file.close()

        audio_stream.stop_stream()
        audio_stream.close()
        self.p.terminate()
        connection.close()


conn = AudioSender()
conn.send_data()
