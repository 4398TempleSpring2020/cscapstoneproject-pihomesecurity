import socket
import threading


class ServerThread(threading.Thread):

    def __init__(self, s):
        threading.Thread.__init__(self)
        self.server = s

    def run(self):
        print("Starting Server Thread...")
        self.server.start()
        print("Ip Address " + self.server.local_address)
        print("Port # " + str(self.server.port))


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


class Server:

    def __init__(self, local_address, port):
        self.local_address = local_address
        self.port = port
        self.listener_threads = []
        self.sender_threads = []
        self.socket_array = []

    def start(self):
        # get the hostname
        ip = self.local_address
        port = self.port
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp.bind((ip, port))

        while True:
            tcp.listen(4)
            print("Waiting for clients connections...")
            (client_socket, (ip, port)) = tcp.accept()
            new_listener_thread = ListenerThread(ip, port, client_socket)
            new_listener_thread.start()
            self.socket_array.append(client_socket)
            self.listener_threads.append(new_listener_thread)

    def send_all(self, str_data):
        try:
            for client_socket in self.socket_array:
                # convert data to json
                client_socket.send(str_data.encode())  # send to server
            return True
        except:
            print("Error sending data")
            return False

    def send(self, index, str_data):
        try:
            self.socket_array[index].send(str_data.encode())  # send to server
            return True
        except:
            print("Error sending data")
            return False


if __name__ == '__main__':
    pi_server = Server(socket.gethostname(), 5000)
    server = ServerThread(pi_server)
    server.start()



