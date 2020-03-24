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
    conn.autocommit(True)
    with conn:
        cur = conn.cursor()
        table = event['table']
        column = event['column']
        value = event['value']
        query = "delete from %s where %s = %s" % (table, column, value)
        #fix the value to have apostrophes if it does not or SQL statement may fail
        if value[0]!="'":
            tempValue = "'" + value + "'"
            value = tempValue
        try:
            cur.execute(query)
        except Exception as e:
            cur.close()
            return {
                "statusCode": 414,
                "error" : str(e)
            }
        result = ""
        #query = "select * from %s where %s = %s" % (table, column, value)
        #cur.execute(query)
        #cur.close()
        #cols = cur.description 
        #result = [{cols[index][0]:col for index, col in enumerate(value)} for value in cur.fetchall()]
        cur.close()
        return {
            'statusCode' : 200,
            'message': "Deleted records successfully",
            'body' : str(result)
        }
