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
#from LogicHandlerThread import LogicHandlerThread



class Driver:
    def __init__(self, q, db):  # add variables to enable sharing with entire program
        self.message_q = q
        self.q_lock = threading.Lock()
        self.db_conn = db
        self.is_armed = False
        self.is_alert = False
        self.is_ongoing_threat = False
        
    if __name__ == '__main__':
        db_connection = DbConn(Constant.host, Constant.uname,
                               Constant.password, Constant.db_name)
        #new stuff from jon
        message_q = deque()
        shared_resources = Driver(message_q, db_connection)
        pi_client = Client(Constant.host_ip, Constant.port, shared_resources)
        pi_system_thread = ClientThread(pi_client, shared_resources)
        pi_system_thread.start()
        message_handler_thread = MessageHandlerThread(shared_resources)
        message_handler_thread.start()
        #logic_handler_thread = LogicHandlerThread(shared_resources) #comment out if you do not have sensors
        #logic_handler_thread.start()
        
        #lukes stuff i think
        pi_server = Server(socket.gethostname(), Constant.port)
        server = ServerThread(pi_server)
        server.start()
        
        #more new stuff from jon
        '''shared_resources.q_lock.acquire()
        while len(message_q) > 0:
          print(shared_resources.message_q.pop())
        shared_resources.q_lock.release()'''
        
        #db_connection.test_integration()
        '''
        ret_dict = ast.literal_eval(
            "{'microphone': ['123/1585615830.5592604/microphone/audio.wav'], "
            "'camera': ['123/1585615830.5592604/camera/image_0.jpg', '123/1585615830.5592604/camera/image_1.jpg',"
            "'123/1585615830.5592604/camera/image_2.jpg', '123/1585615830.5592604/camera/image_3.jpg', "
            "'123/1585615830.5592604/camera/image_4.jpg', '123/1585615830.5592604/camera/image_5.jpg', "
            "'123/1585615830.5592604/camera/image_6.jpg', '123/1585615830.5592604/camera/image_7.jpg', "
            "'123/1585615830.5592604/camera/image_8.jpg', '123/1585615830.5592604/camera/image_9.jpg'],"
            "'ultrasonic': ['123/1585615830.5592604/ultrasonic/ultra.txt'],"
            " 'bucket': 'whateverworks', "
            "'instance_id': '1585615830.5592604',"
            " 'face_match_flag': False, "
            "'wasAlert': True, "
            "'trigger_sensor_type': ['camera']}")
        '''


        print("------------- START SENSORS ---------------")
        ret_dict = run_everything(11)
        print("------------- DONE SENSORS ---------------")

        
        incident_id = str(ret_dict["instance_id"])
        face_match_flag = str(ret_dict["face_match_flag"])
        image_path = ret_dict["camera"]
        mic_path = ret_dict["mic"][0]
        ultrasonic_path = ret_dict["ultrasonic"][0]
        
        temp = IncidentData(11, incident_id, 1, image_path, mic_path, ultrasonic_path)
        print(db_connection.insert_incident_data(temp))
        #ret_dict = run_everything(123)

        print('COMPLETED')