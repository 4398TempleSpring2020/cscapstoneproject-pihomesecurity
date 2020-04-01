#!/usr/bin/python
import os
import sys

sys.path.append('..')

import ast

import pymysql

from Constants.Constant import Constant
from DbConnection.IncidentData import IncidentData
from run_sensors import run_everything

class DbConn:
    # host = None  # "my-pi-database.cxfhfjn3ln5w.us-east-2.rds.amazonaws.com"
    # uname = None  # "pi_user"
    # password = None  # "totallysecurepw!"
    # db_name = None  # "mypidb"
    # connection = None

    def __init__(self, host, uname, password, db_name):
        pymysql.install_as_MySQLdb()
        self.host = host
        self.uname = uname
        self.password = password
        self.db_name = db_name
        self.connection = self.connect()

    def connect(self):
        # Open database connection
        connect_timeout = 5
        db = pymysql.connect(self.host, self.uname, self.password, self.db_name)
        return db

    def disconnect(self):
        # disconnect from server
        self.connection.close()

    def test(self):
        # prepare a cursor object using cursor() method
        cursor = self.connection.cursor()

        # execute SQL query using execute() method.
        cursor.execute("SELECT VERSION()")

        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        print("Database version : %s " % data)

    def insert_incident_data(self, incident_data):
        """
        This function fetches content from mysql RDS instance
        """        result = []
        self.connection.autocommit(True)
        with self.connection.cursor() as cur:

            insert_statement = "INSERT INTO IncidentData (AccountID, IncidentID, FriendlyMatchFlag, ImagePaths, MicrophonePath, UltrasonicPath) "
            insert_data = "('" + incident_data.account_id + "', '" + incident_data.incident_id + "', '" + incident_data.match_flag + "', '" + incident_data.image_path + "', '" + incident_data.mic_path + "', '" + incident_data.sonic_path) + "')"
            insert_statement2 = insert_statement + " VALUES " + insert_data 
            try:
                cur.execute(insert_statement2)
            except Exception as e:
                cur.close()
                return {
                    "statusCode": 412,
                    "error": str(e)
                }
            cur.close()
            self.disconnect()
            return {
                'statusCode': 200,
                'message': "Inserted records successfully",
                'body': ""
            }

    def test_integration(self):
        # time.sleep(2)


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

        #ret_dict = run_everything(123)
        incident_id = str(ret_dict["instance_id"])
        face_match_flag = str(ret_dict["face_match_flag"])
        image_path = ret_dict["camera"]
        mic_path = ret_dict["microphone"][0]
        ultrasonic_path = ret_dict["ultrasonic"][0]

        temp = IncidentData(Constant.ACCOUNT_ID, incident_id, 1, image_path, mic_path,ultrasonic_path)
        print(self.connection.insert_incident_data(temp))
