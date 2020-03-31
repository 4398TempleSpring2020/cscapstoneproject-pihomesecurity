#!/usr/bin/python

import pymysql


class DbConn:
    host = None  # "my-pi-database.cxfhfjn3ln5w.us-east-2.rds.amazonaws.com"
    uname = None  # "pi_user"
    password = None  # "totallysecurepw!"
    db_name = None  # "mypidb"
    connection = None

    def __init__(self, host, uname, password, db_name):
        pymysql.install_as_MySQLdb()
        self.host = host
        self.uname = uname
        self.password = password
        self.db_name = db_name

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



# if __name__ == '__main__':
#     host = "my-pi-database.cxfhfjn3ln5w.us-east-2.rds.amazonaws.com"
#     uname = "pi_user"
#     password = "totallysecurepw!"
#     db_name = "mypidb"
#     print("hello")
#     dbconn = DbConn(host, uname, password, db_name)
#     dbconn.connection = dbconn.connect()
#     dbconn.test()
#     print(dbconn.insert_incident(1,1))
#     dbconn.disconnect()
