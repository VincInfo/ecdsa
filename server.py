from random import SystemRandom
import socket
import struct
from ecdsa import ECDSA, sign

BLOCK_SIZE = 1024
server_host = '127.0.0.1'
server_port = 12345

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


def receive_file(sck: socket.socket, filename):
    filesize = receive_file_size(sck)

    with open(filename, "wb") as f:
        received_bytes = 0
        while received_bytes < filesize:
            chunk = sck.recv(BLOCK_SIZE)
            if chunk:
                # print(chunk) # b'This is very confidential' (bytes literal, each character is a 8 bit value of UTF-8 or ASCII symbol)
                f.write(chunk)
                received_bytes += len(chunk)
            print(chunk, received_bytes, filesize)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((server_host, server_port))

server_socket.listen(1)
print('Server läuft und wartet auf Verbindung...')

while True: 
    client_socket, client_address = server_socket.accept()
    print(f'Verbunden mit: {client_address}')
    data = client_socket.recv(1024)
    filename = data.decode()
    print(f'preparing to send {filename}')
    private_key = SystemRandom().randint(1, ECDSA.n-1)
    signature = sign(private_key, filename)
    
    print(signature)
    client_socket.sendall(signature)

# with socket.create_server(("localhost", 6190)) as server:
#     while 1:
#         print("Waiting for the client...")
#         conn, address = server.accept()
#         print(f"{address[0]}:{address[1]} connected.")
#         print("Receiving file...")
#         receive_file(conn, "message-received.txt")
#         print("File received.")

# print("Connection closed.")

# print()