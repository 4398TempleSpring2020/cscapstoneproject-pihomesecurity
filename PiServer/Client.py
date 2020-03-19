import socket
import sys


class Client:
    port = None
    host = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        host = socket.gethostbyname(self.host)  # argv[1] --> up address of server. Works locally
        port = self.port  # port #
        client_socket = socket.socket()
        client_socket.connect((host, port))  # connect

        message = input(" -> ")

        while message.lower().strip() != 'bye':
            client_socket.send(message.encode())  # send to server
            data = client_socket.recv(2048).decode()  # receive data. 2048 byte max

            print('Received from server: ' + data)

            message = input(" -> ")

        client_socket.close()  # close connection


if __name__ == '__main__':
    client_test = Client(str(sys.argv[1]), 5000)
    client_test.connect()
