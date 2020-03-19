import socket


class PiServer:
    local_address = None
    port = None

    def __init__(self, local_address, port):
        self.local_address = local_address
        self.port = port

    def connect(self):
        # get the hostname
        local_address = self.local_address
        print("local address resolved to: " + socket.gethostbyname(socket.gethostname()))
        host = socket.gethostbyname(str(local_address))
        port = self.port  # port #

        server_socket = socket.socket()  # get instance
        server_socket.bind((host, port))  # bind
        server_socket.listen(2)  # handles 2 connections
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        while True:
            # receive data. 2048 byte max
            data = conn.recv(2048).decode()
            if not data:
                break
            print("from connected user: " + str(data))
            data = input(' -> ')
            conn.send(data.encode())  # send to client

        conn.close()  # close connection


if __name__ == '__main__':
    print("i got " + socket.gethostname())
    print("i got " + socket.gethostbyname(socket.gethostname()))
    server = PiServer(socket.gethostname(), 5000)
    server.connect()
