import socket
import threading
import ast
import time
from PiServer.Constants.Constant import Constant
from PiServer.DbConnection.DbConn import DbConn
from PiServer.DbConnection.IncidentData import IncidentData
from PiServer.Socket.Server import Server, ServerThread


class Driver:

    if __name__ == '__main__':

        db_connection = DbConn(Constant.host, Constant.uname, Constant.password, Constant.db_name)
        db_connection.connection = db_connection.connect()
        pi_server = Server(socket.gethostname(), Constant.port)
        server = ServerThread(pi_server)
        server.start()
        # db_connection.test_integration()
