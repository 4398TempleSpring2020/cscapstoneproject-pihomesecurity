import boto3
import pymysql
import sys
from dateutil import tz
from datetime import datetime

REGION = 'region'

rds_host  = "host"
name = "username"
password = "password"
db_name = "database"

def lambda_handler(event, context):
    session = boto3.Session(region_name="us-east-1")
    sns = session.client('sns')
    result = []
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    homeID = event['homeID']
    homeAddress = ""
    newDateTime = ""
    incidentPhoneNumber = ""
    with conn:
        cur = conn.cursor()
        select_part = "SELECT DISTINCT ha.HomeAccountAddress, ia.DateRecorded, ia.IncidentID, ha.IncidentPhoneNumber "
        table_part = "FROM HomeAccount ha JOIN IncidentData ia "
        where_part = "WHERE ia.AccountID=ha.AccountID AND ha.AccountID=%s ORDER BY ia.DateRecorded DESC" % (homeID)
        query = select_part + table_part + where_part
        #print(query)
        try:
            cur.execute(query)
        except Exception as e:
            cur.close()
            return {
                "error" : str(e)
            }
        result = cur.fetchone()
        incidentID = result[2]
        query = "UPDATE IncidentData SET EmergencyContactedFlag=1 WHERE IncidentID=%s" % (incidentID)
        try:
            cur.execute(query)
        except Exception as e:
            cur.close()
            return {
                "error" : str(e)
            }
        #print(result)
        cur.close()
    homeAddress = result[0]
    newDateTime = result[1]
    incidentPhoneNumber = result[3]
    #print(newDateTime)
    newDateTime = convert_to_est(str(newDateTime))
    #print(newDateTime)
    incAlertMessage = "A break-in was recorded at home address " + homeAddress + " at " + newDateTime + " EST by home security system PiHomeSecurity. \nPlease investigate immediately."
    number = "+12679803862"
    #number = incidentPhoneNumber
    response = sns.publish(
        PhoneNumber = number,
        Message =  incAlertMessage
    )
    return {
        "status": "Successfully sent sms alert to users for incident detected"   
    }

def convert_to_est(date_string):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    utc = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    eastern = utc.astimezone(to_zone)
    return eastern.strftime('%m-%d-%Y %H:%M:%S')
