# A lambda function to interact with AWS RDS MySQL
# updates a specific record in a table in the database

import pymysql
import sys

REGION = 'region'

rds_host  = "rds_host"
name = "name"
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
        table = event['table']
        column = event['column']
        newColVal = event['newColVal']
        row = event['row']
        rowVal = event['rowVal']
        updateStatement = "UPDATE %s set %s = %s WHERE %s = %s" % (table, column, newColVal, row, rowVal)
        try:
            cur.execute(updateStatement)
        except Exception as e:
            cur.close()
            print("Could not update record:" + str(e))
            return {
                "error" : str(e)
            }
        query = "select * from %s where %s = %s" % (table, row, rowVal)
        cur.execute(query)
        cols = cur.description 
        result = [{cols[index][0]:col for index, col in enumerate(value)} for value in cur.fetchall()]
        cur.close()
        return {
            'statusCode' : 200,
            'message': "Updated records successfully",
            'body' : str(result)
        }
