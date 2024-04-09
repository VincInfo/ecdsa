import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))  
    client.sendall(b"Hallo Server!")  
    data = client.recv(1024)  
    print("Antwort vom Server erhalten: ", data.decode())
    client.close()

start_client()