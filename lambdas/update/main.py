# A lambda function to interact with AWS RDS MySQL

import pymysql
import sys

REGION = 'us-east-1'

rds_host  = "my-pi-database.cxfhfjn3ln5w.us-east-2.rds.amazonaws.com"
name = "update_user"
password = "pidb777!"
db_name = "mypidb"

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
        #fix the rowVal to have apostrophes if it does not or SQL statement may fail
        if rowVal[0]!="'":
            tempValue = "'" + rowVal + "'"
            rowVal = tempValue
        updateStatement = "UPDATE %s set %s = %s WHERE %s = %s" % (table, column, newColVal, row, rowVal)
        try:
            cur.execute(updateStatement)
        except Exception as e:
            cur.close()
            return {
                "statusCode": 415,
                "error" : str(e)
            }
        result = ""
        #query = "select * from %s where %s = %s" % (table, row, rowVal)
        #cur.execute(query)
        #cols = cur.description 
        #result = [{cols[index][0]:col for index, col in enumerate(value)} for value in cur.fetchall()]
        #cur.close()
        return {
            'statusCode' : 200,
            'message': "Updated records successfully",
            'body' : str(result)
        }
