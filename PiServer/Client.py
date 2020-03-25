import socket
import sys
import threading


class ListenerThread(threading.Thread):
    local_address = None
    port = None
    socket = None

    def __init__(self, local_address, port, client_socket):
        threading.Thread.__init__(self)
        self.local_address = local_address
        self.port = port
        self.client_socket = client_socket

    def run(self):
        print("Thread " + str(threading.get_ident()) + " handling listener side connection from : "
              + self.local_address + ":" + str(self.port))

        while True:
            # receive data. 2048 byte max
            try:
                data = self.client_socket.recv(2048).decode()
                if not data:
                    break
                print("received data: " + str(data))
            except:
                print("connection error. closing connection")
                break


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.listener_thread = []

    def connect(self):
        host = socket.gethostbyname(self.host)  # argv[1] --> up address of server. Works locally
        port = self.port  # port #
        self.client_socket = socket.socket()
        self.client_socket.connect((host, port))  # connect
        new_listener_thread = ListenerThread(self.host, self.port, self.client_socket)
        new_listener_thread.start()
        self.listener_thread.append(new_listener_thread)

    def send(self, str_data):
        try:
            self.client_socket.send(str_data.encode())  # send to server
            return True
        except:
            print("Error sending data")
            return False


if __name__ == '__main__':
    client_test = Client(str(sys.argv[1]), 5000)
    client_test.connect()



