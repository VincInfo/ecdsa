import os
import queue
from random import SystemRandom
import select
import signal
import socket
import struct
import pickle
import sys
import threading
from ecdsa import ECDSA, sign, verify

BLOCK_SIZE = 1024
# message_queue = queue.Queue()
# running = True

class Message:
    def __init__(self, public_key, text, signature):
        self.public_key = public_key
        self.text = text
        self.signature = signature

class MessageHandler:
    conn = None
    addr = None
    threads = []
    conn = None
    other_name = None

    def __init__(self, name, host, port=None):
        self.name = name
        self.host = host
        self.port = port
        self.shutdown_event = threading.Event()
        self.private_key = SystemRandom().randint(1, ECDSA.n-1)
        self.public_key = self.private_key * ECDSA.G
        signal.signal(signal.SIGINT, self.signal_handler)

    def accept(self):
        self.start_accept()
        self.start_chat()

    def connect(self, host, port):
        self.start_connect(host, port)
        self.start_chat()

    def start_chat(self):
        listen_thread = threading.Thread(target=self.start_listen, daemon=True)
        input_thread = threading.Thread(target=self.start_input, daemon=True)

        self.threads.append(listen_thread)
        self.threads.append(input_thread)

        listen_thread.start()
        input_thread.start()

        [thread.join() for thread in self.threads]

        print("all threads joined")

    def send_message(self, text):
        signature = sign(self.private_key, text)
        message = Message(self.public_key, text, signature)
        serialized_message = pickle.dumps(message)
        self.conn.sendall(serialized_message)

    def receive_file_size(sck: socket.socket):
        fmt = "<Q"
        expected_bytes = struct.calcsize(fmt)
        print(fmt, expected_bytes) # <Q 8
        received_bytes = 0
        stream = bytes()
        while received_bytes < expected_bytes:
            chunk = sck.recv(expected_bytes - received_bytes)
            stream += chunk
            received_bytes += len(chunk)
            print(chunk, stream, received_bytes) # b'\x19\x00\x00\x00\x00\x00\x00\x00' b'\x19\x00\x00\x00\x00\x00\x00\x00' 8
        filesize = struct.unpack(fmt, stream)[0]
        print(filesize) # 25 bytes
        return filesize

    def receive_file(self, sck: socket.socket, filename):
        filesize = self.receive_file_size(sck)

        with open(filename, "wb") as f:
            received_bytes = 0
            while received_bytes < filesize:
                chunk = sck.recv(BLOCK_SIZE)
                if chunk:
                    # print(chunk) # b'This is very confidential' (bytes literal, each character is a 8 bit value of UTF-8 or ASCII symbol)
                    f.write(chunk)
                    received_bytes += len(chunk)
                print(chunk, received_bytes, filesize)

    def start_accept(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.bind((self.host, self.port))
        conn.listen(1)
        print('Waiting for connection...')
        conn, addr = conn.accept()
        self.conn = conn
        self.addr = addr
        data = self.conn.recv(1024)
        self.other_name = data.decode()
        self.conn.sendall(self.name.encode())
        print(f'Connected with: {self.other_name} at {addr}')
        
    def start_connect(self, host, port):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Connecting...')
        conn.connect((host, port))
        addr = f'(\'{host}\', {port})'
        self.conn = conn
        self.addr = addr
        self.conn.sendall(self.name.encode())
        data = self.conn.recv(1024)
        self.other_name = data.decode()
        print(f'Connected with: {self.other_name} at {addr}')

    def start_listen(self):
        # global running
        try:
            while not self.shutdown_event.is_set(): 
                try:
                    data = self.conn.recv(1024)
                    if not data:
                        break
                    message = pickle.loads(data)
                    is_valid = verify(message.public_key, message.text, message.signature)
                    print(f'verifying message: {is_valid}')
                    if message.text.lower() == 'exit()':
                        break
                    print(f'[{self.other_name}]: {message.text}')
                except Exception as e:
                    if not self.shutdown_event.is_set():
                        print(f'Error in start_listen: {e}')
                    break
        finally:
            print("connection closed in start_listen")
            self.conn.close()   
            self.shutdown_event.set()

    def start_input(self):
        # global running
        try:
            while not self.shutdown_event.is_set():
                try:
                    user_input = sys.stdin.readline().strip()
                    # self.conn.sendall(user_input.encode())
                    sys.stdout.write('\033[F\033[K') 
                    sys.stdout.flush()
                    self.send_message(user_input)
                    if user_input.lower() == 'exit()':
                        break
                    print(f'[You]: {user_input}')
                except Exception as e:
                    if not self.shutdown_event.is_set():
                        print(f'Error in start_input: {e}')
                    break
        finally:
            print("connection closed in start_input")
            self.conn.close()
            self.shutdown_event.set()
            print("connection closed in start_input done")

    def signal_handler(self, sig, frame):
        print("Shutting down all threads gracefully")
        self.shutdown_event.set()
        self.conn.close()

    # def signal_handler(sig, frame):
    #     print("Received interrupt signal. Shutting down gracefully...")
    #     global running
    #     running = False 
