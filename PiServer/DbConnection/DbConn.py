#!/usr/bin/python

import pymysql


class DbConn:
    host = None  # "my-pi-database.cxfhfjn3ln5w.us-east-2.rds.amazonaws.com"
    uname = None  # "admin"
    password = None  # "root1234"
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

    def send_data(self):
        # code to send data to db
        print("writing to db")
        # prepare a cursor object using cursor() method
        cursor = self.connection.cursor()

        # Prepare SQL query to INSERT a record into the database.
        sql = "INSERT INTO EmployeeHomeRelationship(EmployeeId, \
               AccountId, AccessDate) \
               VALUES ('%s, %s, '%s')"  # % \
        # (data.EmployeeId, data.AccountId, data.AccessDate, 'M', 2000)
        # https://stackoverflow.com/questions/1136437/inserting-a-python-datetime-datetime-object-into-mysql

        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            self.connection.commit()
        except:
            # Rollback in case there is any error
            self.connection.rollback()


if __name__ == '__main__':
    host = "my-pi-database.cxfhfjn3ln5w.us-east-2.rds.amazonaws.com"
    uname = "admin"
    password = "root1234"
    db_name = "mypidb"

    dbconn = DbConn(host, uname, password, db_name)
    dbconn.connection = dbconn.connect()
    dbconn.test()
    dbconn.disconnect()
