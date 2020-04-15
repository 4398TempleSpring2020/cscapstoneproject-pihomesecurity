from datetime import datetime
import pymysql
import sys
import json
from time import sleep
from dateutil import tz
import base64
import os
import urllib
from urllib import request, parse

REGION = 'region'

rds_host  = "host"
name = "username"
password = "password"
db_name = "database"
mybucket = "bucket"

TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

def lambda_handler(event, context):
    result = []
    phonenums = []
    homeAddress = ""
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    eventTime = event['Records'][0]['eventTime']
    eventName = event['Records'][0]['eventName']
    ipAddress = event['Records'][0]['requestParameters']['sourceIPAddress']
    #error = 0
    #eventMessage = "event name: " + eventName + ", event time: " + eventTime + ", ip address: " + ipAddress
    #s3Message = "file: " + key + ", bucket: " + bucket
    if bucket == mybucket and "Put" in eventName and "faces" not in key and "camera" in key: #and ipAddress==myipaddress:
        #print(bucket)
        keys = key.split('/')
        #print(keys)
        homeID=keys[0]
        #incidentID=keys[1]
        #print(incidentID)
        #print(homeID)
        image = keys[len(keys)-1]
        if "image_9" in image:
            #print(image)
            conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
            with conn:
                cur = conn.cursor()
                '''query = "SELECT FriendlyMatchFlag, BadIncidentFlag FROM IncidentData WHERE IncidentID = '%s'" % (incidentID)
                for i in range(0,5):
                    try:
                        cur.execute(query)
                        result = cur.fetchone()
                        print(result)
                    except Exception as e:
                        print(e)
                    if result is not None:
                        break
                    else:
                        sleep(0.4)
                if result is not None:
                    if result[1]==0 and result[0]==1:
                        return {
                            "status":"Not sending sms to user; friendly match flag is true and bad incident flag is false"
                            }
                if result is None:
                    error = -1
                    '''
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
                #print(row)
                phonenums.append("+1" + str(row[0]))
            #print(phonenums)
            homeAddress = result[0][1]
            #print(homeAddress)
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
            newDateTime = ""
            try:
                #print(eventTime)
                tokens = eventTime.split("T")
                dates = tokens[0].split("-")
                newDateTime = dates[1] + "-" + dates[2] + "-" + dates[0]
                times = tokens[1].split(":")
                times2 = times[2].split(".")
                newTime = times[0] + ":" + times[1] + ":" + times2[0]
                newDateTime = newDateTime + " " + newTime
                #print(newDateTime)
                newDateTime = convert_to_est(newDateTime)
            except Exception as e:
                print(str(e))
                newDateTime = eventTime
            #print(newDateTime)
            incAlertMessage = "An incident was detected by PiHomeSecurity at " + newDateTime + " EST at home address " + newAddress + ". "
            appNotMessage = "Please open the PiHomeSecurityMobile app and take action within the next 5 minutes or the authorities will be contacted."
            #incErrorMessage = "A possible incident was detected by PiHomeSecurity at " + newDateTime + " EST at home address " + newAddress + " but something went wrong. "
            #incErrorMessage2 = "Please contact the PiHomeSecurity Administration for help."
            #print(incAlertMessage + "\n" + appNotMessage)
            body = incAlertMessage + appNotMessage
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
            
def convert_to_est(date_string):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    utc = datetime.strptime(date_string, '%m-%d-%Y %H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    eastern = utc.astimezone(to_zone)
    return eastern.strftime('%m-%d-%Y %H:%M:%S')
