# sys.path.append('...')
import ast
import socket
import threading
import time
from collections import deque

from DbConn import DbConn
from Constant import Constant
from Client import Client
from Client import ClientThread
from MessageHandlerThread import MessageHandlerThread
from LogicHandlerThread import LogicHandlerThread

class Driver:
    
    def __init__(self, q, db):          # add variables to enable sharing with entire program
        self.message_q = q              # queue for holding response from mobile
        self.q_lock = threading.Lock()  # lock for q sync
        self.db_conn = db               # connection to database
        self.is_armed = False           # is system armed?
        self.was_alert = False          # comes lukes code on run everything return
        self.is_ongoing_threat = False  # is there a ongoing threat?
        self.record_incident = False    # should i record incident?
   

if __name__ == '__main__':
    # global shared resources
    message_q = deque()
    db_connection = DbConn(Constant.host, Constant.uname, Constant.password, Constant.db_name)
    shared_resources = Driver(message_q, db_connection)

    pi_client = Client(Constant.host_ip, Constant.port, shared_resources)
    pi_system_thread = ClientThread(pi_client, shared_resources)
    pi_system_thread.start()
    message_handler_thread = MessageHandlerThread(shared_resources)
    message_handler_thread.start()

    #logic_handler_thread = LogicHandlerThread(shared_resources)    # comment out if you do not have sensors
    #logic_handler_thread.start()                                   # comment out if you do not have sensors
