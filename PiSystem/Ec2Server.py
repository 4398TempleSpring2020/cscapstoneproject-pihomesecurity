# sys.path.append('...')
import ast
import socket
from Server import Server
from Server import ServerThread
from Constant import Constant
# from PiSystem.run_sensors import run_everything

'''
Public DNS (IPv4): ec2-3-16-163-252.us-east-2.compute.amazonaws.com
IPv4 Public IP: 3.16.163.252
'''


class Ec2Server:
    if __name__ == '__main__':
        host = "3.16.163.252"
        DNS = "ec2-3-16-163-252.us-east-2.compute.amazonaws.com"
        pi_server = Server(socket.gethostname(), Constant.port)
        server = ServerThread(pi_server)
        server.start()
        # db_connection.test_integration()
