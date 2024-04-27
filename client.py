import os
import socket
import struct
from ecdsa import ECDSA, verify

BLOCK_SIZE = 1024
server_host = '127.0.0.1'
server_port = 12345

def send_file(sck: socket.socket, filename):
    filesize = os.path.getsize(filename)
    print(filesize) # 25 bytes
    sck.sendall(struct.pack("<Q", filesize))
    print(struct.pack("<Q", filesize)) # b'\x19\x00\x00\x00\x00\x00\x00\x00'
    with open(filename, "rb") as f:
        while read_bytes := f.read(BLOCK_SIZE):
            sck.sendall(read_bytes)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

# while True:
get_message = './message.txt'
client_socket.sendall(get_message.encode())
signature = client_socket.recv(1024)
print(signature.decode())
client_socket.close()


# with socket.create_connection(("localhost", 6190)) as conn:
#     print("Connected to the server.")
#     print("Sending file...")
#     send_file(conn, "message.txt")
#     print("Sent.")

# print("Connection closed.")