import socket
import threading
import ast
import time
from Constants.Constant import Constant
from DbConnection.DbConn import DbConn
from DbConnection.IncidentData import IncidentData
from Socket.Server import Server, ServerThread
from sensors_all.run_sensors import run_everything

class Driver:

    if __name__ == '__main__':
        #db_connection = DbConn(Constant.host, Constant.uname,
        #                       Constant.password, Constant.db_name)
        db_connection.connection = db_connection.connect()
        pi_server = Server(socket.gethostname(), Constant.port)
        server = ServerThread(pi_server)
        server.start()
        #db_connection.test_integration()
        ret_dict = run_everything(123)
