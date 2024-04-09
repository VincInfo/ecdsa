import socket
import struct


def receive_file_size(sck: socket.socket):
    # This funcion makes sure that the bytes which indicate
    # the size of the file that will be sent are received.
    # The file is packed by the client via struct.pack(),
    # a function that generates a bytes sequence that
    # represents the file size.
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
    # First read from the socket the amount of
    # bytes that will be received from the file.
    filesize = receive_file_size(sck)

    # Open a new file where to store the received data.
    with open(filename, "wb") as f:
        received_bytes = 0
        # Receive the file data in 1024-bytes chunks
        # until reaching the total amount of bytes
        # that was informed by the client.
        while received_bytes < filesize:
            chunk = sck.recv(1024)
            if chunk:
                # print(chunk) # b'This is very confidential' (bytes literal, each character is a 8 bit value of UTF-8 or ASCII symbol)
                f.write(chunk)
                received_bytes += len(chunk)
            print(chunk, received_bytes, filesize)


with socket.create_server(("localhost", 6190)) as server:
    while 1:
        print("Waiting for the client...")
        conn, address = server.accept()
        print(f"{address[0]}:{address[1]} connected.")
        print("Receiving file...")
        receive_file(conn, "message-received.txt")
        print("File received.")

print("Connection closed.")