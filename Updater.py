import socket
# from scipy.io.wavfile import read, write
import io
import queue
import time
from threading import Thread
import numpy as np


class BSUpdater:
    def __init__(self, bs_length: int, ip_address: str, port: int):
        self.bs_length = bs_length
        self.host = ip_address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.queue = queue.Queue()
        print('Initialized')

    def send(self):
        if not self.queue.empty():
            bs_seq = self.queue.get()           # magnified and convolved before putting in the queue
            for frame in bs_seq:
                posString = ','.join(map(str, frame))
                self.sock.sendall(posString.encode("UTF-8"))
                time.sleep(0.03)

    def update(self, bs_seq):
        self.queue.put(bs_seq)
        ts = Thread(target=self.send)
        ts.start()

'''
class VoiceUpdater:
    def __init__(self, ip_address: str, port: int):
        self.host = ip_address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print('Initialized')

    def update(self):
        with open("file.wav", "rb") as wavfile:
            input_wav = wavfile.read()
            # here, input_wav is a bytes object representing the wav object
            rate, data = read(io.BytesIO(input_wav))
            bytes_wav = bytes()
            byte_io = io.BytesIO(bytes_wav)
            write(byte_io, rate, data)  # received_data
            output_wav = byte_io.read()  # and back to bytes, tadaaa
            # output_wav can be written to a file, of sent over the network as a binary
            self.sock.sendall(output_wav)
            print('Sent!')

'''
if __name__ == '__main__':
    updater = BSUpdater(52, '127.0.0.1', port=25001)
    bs = np.load('data.npz')['arr_0']*1.5
    while True:
        updater.update(bs)
        time.sleep(5)
    # voice_updater = VoiceUpdater('127.0.0.1', port=25003)
    # voice_updater.update()

