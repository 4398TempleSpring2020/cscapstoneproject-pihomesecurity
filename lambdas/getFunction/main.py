# A lambda function to interact with AWS RDS MySQL
# retrieves all tables in database

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
        query = "show tables"
        try:
            cur.execute(query)
        except Exception as e:
            cur.close()
            return {
                "statusCode": 410,
                "error": str(e)
            }
        cols = cur.description 
        result = [{cols[index][0]:col for index, col in enumerate(value)} for value in cur.fetchall()]
        cur.close()
        return {
            'statusCode' : 200,
            'message': "Get request successful",
            'body' : result
        }
