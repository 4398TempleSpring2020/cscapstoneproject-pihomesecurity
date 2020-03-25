# A lambda function to interact with AWS RDS MySQL
# retrieve a specific record from a table in the database

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
        columns = event['columns']
        columnMatch = event['columnMatch']
        valueMatch = event['valueMatch']
        query = "select %s from %s where %s = %s" % (columns, table, columnMatch, valueMatch)
        try:
            cur.execute(query)
        except Exception as e:
            cur.close()
            print(str(e))
            return {
                "error" : str(e)
            }
        cols = cur.description 
        result = [{cols[index][0]:col for index, col in enumerate(value)} for value in cur.fetchall()]
        cur.close()
        return {
            'statusCode' : 200,
            'message': "Retrieved records successfully",
            'body' : str(result)
        }
