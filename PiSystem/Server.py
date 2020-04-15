#!/usr/bin/python
import socket
import sys
import threading


class ServerThread(threading.Thread):

    def __init__(self, s):
        threading.Thread.__init__(self)
        self.server = s

    def run(self):
        print("Starting Server Thread...")
        self.server.start()


class ListenerThread(threading.Thread):
    local_address = None
    port = None
    socket = None

    def __init__(self, local_address, port, client_socket, server):
        threading.Thread.__init__(self)
        self.local_address = local_address
        self.port = port
        self.client_socket = client_socket
        self.server = server

    def run(self):
        print("Thread " + str(threading.get_ident()) + " handling listener side connection from : "
              + self.local_address + ":" + str(self.port))
        placed = False

        while True:
            # receive data. 2048 byte max
            try:
                data = self.client_socket.recv(2048).decode()
                if not data:
                    break
                    #aquire lock
                if placed is False:
                    if str(data) == "PI_System" and self.server.pi_socket is None:
                        self.server.pi_socket = self.client_socket
                        print("Pi System connected")
                        placed = True
                    if str(data) == "Pi_Mobile":
                        self.server.mobile_socket_array.append(self.client_socket)
                        print("Mobile connected")
                        placed = True

                    if str(data) == "Pi_Mobile_Admin" and self.server.admin_socket is None:
                        self.server.admin_socket = self.client_socket
                        print("Mobile Admin connected")
                        placed = True

                    if str(data) != "Pi_Mobile" and str(data) != "PI_System" and str(data) != "Pi_Mobile_Admin":
                        print("connection rejected unknown client attempting to connect")
                        self.client_socket.close()
                        #remove
                        #release lock
                        sys.exit()

                print("received data: " + str(data))
                ## if comes from mobile send to Pi
                self.server.send_to_pi(str(data))

            except:
                print("connection error. closing connection")
                break


class Server:

    def __init__(self, local_address, port):
        self.local_address = local_address
        self.port = port
        self.listener_threads = []
        self.mobile_socket_array = []
        self.pi_socket = None
        self.admin_socket = None

    def start(self):
        # get the hostname
        ip = socket.gethostbyname(self.local_address)
        port = self.port
        print("Ip Address " + ip)
        print("Port # " + str(port))
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp.bind((ip, port))

        while True:
            tcp.listen()
            print("Waiting for clients connections...")
            (client_socket, (ip, port)) = tcp.accept()
            new_listener_thread = ListenerThread(ip, port, client_socket, self)
            new_listener_thread.start()
            self.mobile_socket_array.append(client_socket)
            self.listener_threads.append(new_listener_thread)

    def send_all_mobile_users(self, str_data):
        try:
            for client_socket in self.mobile_socket_array:
                # convert data to json
                client_socket.send(str_data.encode())  # send to server
            return True
        except:
            print("Error sending data")
            return False

    def send_specified_mobile(self, index, str_data):
        try:
            # convert data to json
            self.mobile_socket_array[index].send(str_data.encode())  # send to server
            return True
        except:
            print("Error sending data")
            return False

    def send_admin_mobile(self, index, str_data):
        try:
            # convert data to json
            self.admin_socket[index].send(str_data.encode())  # send to server
            return True
        except:
            print("Error sending data")
            return False

    def send_to_pi(self, str_data):
        try:
            self.pi_socket.send(str_data.encode())  # send to server
            return True
        except:
            print("Error sending data")
            return False
