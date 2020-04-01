#!/usr/bin/python
import ast

import pymysql

from PiServer.Constants.Constant import Constant
from PiServer.DbConnection.IncidentData import IncidentData


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
        """
        result = []
        self.connection.autocommit(True)
        with self.connection.cursor() as cur:

            insert_statement = 'INSERT INTO IncidentData (AccountID, SensorFile, ImagePath) VALUES (%s, %s, %s)'
            insert_data = (int(incident_data.account_id), incident_data.sensor_path, incident_data.image_path,)
            try:
                cur.execute(insert_statement, insert_data)
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

        image_path = str(ret_dict["camera"])
        mic_path = ret_dict["microphone"][0]
        ultrasonic_path = ret_dict["ultrasonic"][0]

        temp = IncidentData(Constant.ACCOUNT_ID, image_path, mic_path)
        print(self.connection.insert_incident_data(temp))
