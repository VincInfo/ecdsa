import os
import socket
import struct


def send_file(sck: socket.socket, filename):
    # Get the size of the outgoing file.
    filesize = os.path.getsize(filename)
    print(filesize) # 25 bytes
    # First inform the server the amount of
    # bytes that will be sent.
    sck.sendall(struct.pack("<Q", filesize))
    print(struct.pack("<Q", filesize)) # b'\x19\x00\x00\x00\x00\x00\x00\x00'
    # Send the file in 1024-bytes chunks.
    with open(filename, "rb") as f:
        while read_bytes := f.read(1024):
            sck.sendall(read_bytes)


with socket.create_connection(("localhost", 6190)) as conn:
    print("Connected to the server.")
    print("Sending file...")
    send_file(conn, "message.txt")
    print("Sent.")

print("Connection closed.")