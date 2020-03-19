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
        table = event['table']
        columns = event['columns']
        columnMatch = event['columnMatch']
        valueMatch = event['valueMatch']
        #fix the valueMatch to have apostrophes if it does not or SQL statement may fail
        if valueMatch[0]!="'":
            tempValue = "'" + valueMatch + "'"
            valueMatch = tempValue
        #if column we are matching is HomeAccountAddress for user login, we will change our syntax to LIKE instead of =
        if columnMatch == "HomeAccountAddress":
            tempValue = valueMatch[:-1]
            tempValue += "%'"
            valueMatch = tempValue
            query = "select %s from %s where %s LIKE %s" % (columns, table, columnMatch, valueMatch)
            #print(query)
        else:
            query = "select %s from %s where %s = %s" % (columns, table, columnMatch, valueMatch)
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
        
