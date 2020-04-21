import socket
import sys
import threading
import time
from collections import deque


class ClientThread(threading.Thread):

    def __init__(self, c, shared_resources):
        threading.Thread.__init__(self)
        self.client = c
        self.shared_resources = shared_resources

    def run(self):
        print("Starting Client Thread...")
        self.client.connect()
        time.sleep(5)  # small delay to prevent read b4 write
        self.client.send("PI_System")  # some unique string so server knows we are who we say we are


class ListenerThread(threading.Thread):
    local_address = None
    port = None
    socket = None

    def __init__(self, local_address, port, client_socket, shared_resources):
        threading.Thread.__init__(self)
        self.local_address = local_address
        self.port = port
        self.server_socket = client_socket
        self.shared_resources = shared_resources

    def run(self):
        print("Thread " + str(threading.currentThread().ident) + " handling listener side connection from : "
              + self.local_address + ":" + str(self.port))
        while True:
            # receive data. 2048 byte max
            try:
                data = self.server_socket.recv(2048).decode()
                if not data:
                    break
            except:
                print("connection error. closing connection")
                #try to send message again?
                break

            #print("received data: " + str(data))  # test
            self.shared_resources.q_lock.acquire()  # get lock
            self.shared_resources.message_q.appendleft(str(data))
            self.shared_resources.q_lock.release()  # release lock
            time.sleep(3)




class Client:

    def __init__(self, host, port, shared_resources):
        self.host = host
        self.port = port
        self.server_socket = None
        self.shared_resources = shared_resources

    def connect(self):
        host = socket.gethostbyname(self.host)  # argv[1] --> up address of server. Works locally
        port = self.port  # port #
        self.server_socket = socket.socket()
        self.server_socket.connect((host, port))  # connect
        new_thread = ListenerThread(self.host, self.port, self.server_socket, self.shared_resources)
        new_thread.start()

    def send(self, str_data):
        try:
            self.server_socket.send(str_data.encode())  # send to server
            return True
        except:
            print("Error sending data")
            return False

