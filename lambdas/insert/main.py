# A lambda function to interact with AWS RDS MySQL

import pymysql
import sys

REGION = 'us-east-1'

rds_host  = "my-pi-database.cxfhfjn3ln5w.us-east-2.rds.amazonaws.com"
name = "insert_user"
password = "mypi123"
db_name = "mypidb"

def lambda_handler(event, context):
    """
    This function fetches content from mysql RDS instance
    """
    result = []
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    conn.autocommit(True)
    with conn:
        cur = conn.cursor()
        table = event['table']
        columns = event['columns']
        values = event['values']
        insertStatement = "INSERT INTO %s (%s) VALUES (%s)" % (table, columns, values)
        try:
            cur.execute(insertStatement)
        except Exception as e:
            cur.close()
            return {
                "statusCode": 412,
                "error" : str(e)
            }
        cur.close()
        return {
            'statusCode' : 200,
            'message': "Inserted records successfully",
            'body' : ""
        }
