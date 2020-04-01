import os
import sys

sys.path.append('..')

import socket
import threading
import ast
import time
from Constants.Constant import Constant
from DbConnection.DbConn import DbConn
from DbConnection.IncidentData import IncidentData
from Socket.Server import Server, ServerThread
from run_sensors import run_everything

class Driver:

    if __name__ == '__main__':
        db_connection = DbConn(Constant.host, Constant.uname,
                               Constant.password, Constant.db_name)
        pi_server = Server(socket.gethostname(), Constant.port)
        server = ServerThread(pi_server)
        server.start()
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
        ret_dict = run_everything(4)
        incident_id = ret_dict["instance_id"]
        face_match_flag = ret_dict["face_match_flag"]
        image_path = str(ret_dict["camera"])
        mic_path = ret_dict["microphone"][0]
        ultrasonic_path = ret_dict["ultrasonic"][0]

        temp = IncidentData(Constant.ACCOUNT_ID, incident_id, 1, image_path, mic_path, ultrasonic_path)
        print(db_connection.insert_incident_data(temp))
        #ret_dict = run_everything(123)

        print('COMPLETED')
