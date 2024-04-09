import socket

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(1) 
    print("Server gestartet und bereit für Verbindungen.")

    while True:
        conn, addr = server.accept() 
        print(f"Verbindung von {addr} hergestellt.")
        data = conn.recv(1024)
        print("Nachricht vom Client erhalten: ", data.decode())
        conn.sendall(b"Meldung erhalten.")
        conn.close()

start_server()