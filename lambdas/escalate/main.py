import pymysql
import sys
import os
import urllib
from urllib import request, parse
import json

REGION = 'region'

rds_host  = "host"
name = "username"
password = "password"
db_name = "database"


TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

def lambda_handler(event, context):
    result = []
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    homeID = event['homeID']
    phonenums = []
    homeAddress = ""
    incidentID = ""
    incidentDate = ""
    with conn:
        cur = conn.cursor()
        select_part = "SELECT DISTINCT ua.UserPhoneNumber, ha.HomeAccountAddress, ha.NumOfUsers "
        table_part = "FROM HomeAccount ha JOIN UserAccounts ua "
        where_part = "WHERE ua.AccountID=ha.AccountID AND ha.AccountID=%s GROUP BY ua.UserPhoneNumber, ha.HomeAccountAddress, ha.NumOfUsers" % (homeID)
        query = select_part + table_part + where_part
        #print(query)
        try:
            cur.execute(query)
        except Exception as e:
            cur.close()
            return {
                "error" : str(e)
            }
        result = cur.fetchall()
        #print(result)
        cur.close()
    for row in result:
        phonenums.append("+1" + str(row[0]))
    print(phonenums)
    homeAddress = result[0][1]
    addTokens = homeAddress.split(",")
    newAddress = ""
    if addTokens[0] is not None:
        street = addTokens[0].split(" ")
        newAddress = street[0]
        newAddress = newAddress + " *********"
        if len(addTokens)>1 and addTokens[1] is not None:
            newAddress += addTokens[1]
        if len(addTokens)>2 and addTokens[2] is not None:
            noZip = addTokens[2].split(" ")
            if noZip[0] == "":
                if len(noZip)>1 and noZip[1] is not None:
                    newAddress = newAddress + ", " + noZip[1]
                else:
                    newAddress = newAddress + "," + addTokens[2]
            elif noZip[0] is not None:
                newAddress = newAddress + "," + noZip[0]
            else:
                newAddress = newAddress + "," + addTokens[2]
    else:
        newAddress = homeAddress
    #print(newAddress)
    with conn:
        cur = conn.cursor()
        query = "SELECT ia.DateRecorded, ia.IncidentID FROM HomeAccount ha, IncidentData ia WHERE ia.AccountID=ha.AccountID AND ha.AccountID=%s ORDER BY ia.DateRecorded DESC" % (homeID)      
        try:
            cur.execute(query)
        except Exception as e:
            cur.close()
            return {
                "error" : str(e)
            }
        result2 = cur.fetchone()
        incidentID = result2[1]
        incidentDate = result2[0]
        query = "UPDATE IncidentData SET BadIncidentFlag=1 WHERE IncidentID=%s" % (incidentID)
        try:
            cur.execute(query)
        except Exception as e:
            cur.close()
            return {
                "error" : str(e)
            }
        cur.close()
    incAlertMessage = "No response received for the incident detected by PiHomeSecurity at home address " + newAddress + ". "
    appNotMessage = "The incident has been auto-escalated and authorities will be contacted immediately."
    body = incAlertMessage + "\n" + appNotMessage
    for number in phonenums:
        from_number = os.environ.get("FROM_NUMBER")
        populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
        post_params = {"To": number, "From": from_number, "Body": body}
    
        # encode the parameters for Python's urllib
        data = parse.urlencode(post_params).encode()
        req = request.Request(populated_url)
        
        # add authentication header to request based on Account SID + Auth Token
        authentication = "{}:{}".format(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        base64string = base64.b64encode(authentication.encode('utf-8'))
        req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
        try:
            # perform HTTP POST request
            with request.urlopen(req, data) as f:
                print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
        except Exception as e:
            # something went wrong!
            return e
    return {
        "status": "Successfully sent sms alert to users for incident detected"   
    }
