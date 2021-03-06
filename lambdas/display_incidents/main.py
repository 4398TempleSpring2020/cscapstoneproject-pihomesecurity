# A lambda function to interact with AWS RDS MySQL

import pymysql
import sys

REGION = 'region'

rds_host  = "host"
name = "username"
password = "password"
db_name = "database"

def lambda_handler(event, context):
    """
    This function fetches content from mysql RDS instance
    """
    result = []
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    with conn:
        cur = conn.cursor()
        homeID = event['homeID']
        select_part = "SELECT inc.IncidentID, inc.DateRecorded, inc.BadIncidentFlag, inc.ImagePaths, inc.FriendlyMatchFlag, inc.MicrophonePath, inc.UltrasonicPath "
        table_part = "FROM IncidentData inc "
        where_part = "WHERE inc.AccountID=%s ORDER BY inc.DateRecorded DESC" % (homeID)
        query = select_part + table_part + where_part
        #print(query)
        try:
            cur.execute(query)
        except Exception as e:
            cur.close()
            return {
                "statusCode": 413,
                "error" : str(e)
            }
        cols = cur.description 
        result = [{cols[index][0]:col for index, col in enumerate(value)} for value in cur.fetchall()]
        print(result)
        print(result[0])
        cur.close()
        if len(result)>0:
            return {
            'statusCode' : 200,
            'message': "Retrieved records successfully",
            'body' : '[' + str(result[0]) + ']'
            }
        else:
            return {
            'statusCode' : 411,
            'message': "No records found",
            'body' : " "
            }
