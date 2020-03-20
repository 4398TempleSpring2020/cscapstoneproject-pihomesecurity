# A lambda function to interact with AWS RDS MySQL

import pymysql
import sys

REGION = 'us-east-1'

rds_host  = "my-pi-database.cxfhfjn3ln5w.us-east-2.rds.amazonaws.com"
name = "read_user"
password = "temple123"
db_name = "mypidb"

def lambda_handler(event, context):
    """
    This function fetches content from mysql RDS instance
    """
    result = []
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    with conn:
        cur = conn.cursor()
        homeID = event['homeID']
        select_part = "SELECT inc.IncidentID, inc.DateRecorded, inc.BadIncidentFlag, inc.AdminComments, cd.CameraDataID, cd.ImagePath, cd.ImageSize, cd.ImageType, cd.FriendlyMatchFlag, sd.SensorDataID, sd.SensorFile, sd.Length "
        table_part = "FROM IncidentData inc LEFT JOIN CameraData cd ON inc.IncidentID=cd.IncidentID LEFT JOIN SensorData sd ON inc.IncidentID=sd.IncidentID "
        where_part = "WHERE inc.AccountID=%s ORDER BY inc.IncidentID" % (homeID)
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
        cur.close()
        if len(result)>0:
            return {
            'statusCode' : 200,
            'message': "Retrieved records successfully",
            'body' : str(result)
            }
        else:
            return {
            'statusCode' : 411,
            'message': "No records found",
            'body' : str(result)
            }
        
