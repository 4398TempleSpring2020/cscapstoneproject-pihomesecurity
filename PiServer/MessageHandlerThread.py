import threading
import os
import time
import signal
import requests
import subprocess
from Constant import Constant
from subprocess import Popen

class MessageHandlerThread(threading.Thread):

    def __init__(self, shared_resources):
        threading.Thread.__init__(self)
        self.shared_resources = shared_resources
        
        self.URL1 = "https://jlt49k4n90.execute-api.us-east-2.amazonaws.com/beta/contact-police/"
        
        self.URL2 = "https://jlt49k4n90.execute-api.us-east-2.amazonaws.com/beta/alert-response/"
        
    def run(self):
        
        while True:
            
            if len(self.shared_resources.message_q) > 0:
                with self.shared_resources.q_lock:
                    print("Message Handler aquired lock and something in queue")
                    
                    message = self.shared_resources.message_q.pop()
                    print("message received: " + message)

                    if message == "ARM":
                        if self.shared_resources.is_armed is False:
                            self.shared_resources.is_armed = True
                            print("\tResources Set:\tIs Armed: ",self.shared_resources.is_armed)
                            self.shared_resources.is_max_alert = False
                            print("\tResources Set:\tIs Max Alert: ",self.shared_resources.is_max_alert)
                            self.shared_resources.is_active_incident = False   # on arming from a disarmed state set to false
                            print("\tResources Set:\tIs Active Incident: ", self.shared_resources.is_active_incident)
                            self.shared_resources.is_panic = False
                            print("\tResources Set:\tIs Panic: ", self.shared_resources.is_panic)
                            self.shared_resources.response_received = False
                            self.shared_resources.sound_pid=-1
                            print("\tSOUND PID RESET: ",self.shared_resources.sound_pid)
                        elif self.shared_resources.is_armed is True:
                            print("** DISREGARD MESAGE ** system already was armed")
                            
                    elif message == "DISARM":
                        #see which of these works
                        if self.shared_resources.sound_pid >0:
                            os.kill(self.shared_resources.sound_pid, signal.SIGKILL)
                            self.shared_resources.sound_pid = -1
                            print("\tSOUND PID RESET: ",self.shared_resources.sound_pid)
                        
                        if self.shared_resources.is_armed is True:
                            self.shared_resources.is_armed = False
                            print("\tResources Set:\tIs Armed: ", self.shared_resources.is_armed)
                            self.shared_resources.is_max_alert = False
                            print("\tResources Set:\tIs Max Alert: ", self.shared_resources.is_max_alert)
                            self.shared_resources.is_active_incident = False
                            print("\tResources Set:\tIs Acive Incident: ", self.shared_resources.is_active_incident)
                            self.shared_resources.is_panic = False
                            print("\tResources Set:\tIs Panic: ", self.shared_resources.is_panic)
                            self.shared_resources.response_received = False
                        elif self.shared_resources.is_panic is True:
                            self.shared_resources.is_max_alert = False 
                            print("\tResources Set:\tIs Max Alert: ", self.shared_resources.is_max_alert)
                            self.shared_resources.is_active_incident = False
                            print("\tResources Set:\tIs Acive Incident: ", self.shared_resources.is_active_incident)
                            self.shared_resources.is_panic = False
                            print("\tResources Set:\tIs Panic: ", self.shared_resources.is_panic)
                        
                        elif self.shared_resources.is_armed is False:
                            print("** DISREGARD MESAGE ** system already disarmed")
                          

                    elif message == "RESOLVE":
                        if(self.shared_resources.sound_pid>0):
                            os.kill(self.shared_resources.sound_pid, signal.SIGKILL)
                            self.shared_resources.sound_pid = -1
                            print("\tSOUND PID RESET: ",self.shared_resources.sound_pid)
                        if self.shared_resources.is_active_incident is True:
                            self.shared_resources.is_active_incident = False
                            print("\tResources Set:\tIs Active Incident: ",self.shared_resources.is_active_incident)
                            self.shared_resources.is_armed = False
                            print("\tResources Set:\tIs Armed: ", self.shared_resources.is_armed)
                            self.shared_resources.is_panic = False
                            print("\tResources Set:\tIs Panic: ", self.shared_resources.is_panic)
                            self.shared_resources.response_received = True
                        elif self.shared_resources.is_active_incident is False:
                            print("** DISREGARD MESAGE ** no active incident")
                        

                    elif message == "ESCALATE":
                        
                        if self.shared_resources.is_active_incident is True:
                            if self.shared_resources.is_max_alert is False:
                                if self.shared_resources.is_panic is False:
                                    self.shared_resources.response_received = True
                                    self.shared_resources.is_max_alert = True
                                    print("\tResources Set:\tIs Max Alert: ", self.shared_resources.is_max_alert)
                                    #this is for contacting police
                                
                                    data = {'homeID': Constant.ACCOUNT_ID}
                                    #response holds the string returned from POST, if there was an error it should be in here
                                    response = requests.post(self.URL1, json = data)
                                    print("ESCALATE RESPONSE: ",response.text) #this is the response text, should say it was successful in here 

                                    # stop beep
                                    # start siren
                                
                            elif self.shared_resources.is_max_alert is True:
                                print("** DISREGARD MESAGE ** already was escalated/Max Alert -- Police Notified")
                        
                                               

                    elif message == "PANIC":
                        sound = Popen(["aplay", Constant.SIREN])
                        self.shared_resources.sound_pid = sound.pid
                        print("\t\tSOUND PID: ",self.shared_resources.sound_pid)
                        self.shared_resources.is_active_incident = False
                        print("\tResources Set:\tIs Active Incident: ", self.shared_resources.is_max_alert)
                        self.shared_resources.is_max_alert = True
                        print("\tResources Set:\tIs Max Alert: ", self.shared_resources.is_max_alert)
                        self.shared_resources.is_panic = True
                        print("\tResources Set:\tIs Panic: ", self.shared_resources.is_panic)
                        # contact police
                        data = {'homeID': Constant.ACCOUNT_ID}
                        #response holds the string returned from POST, if there was an error it should be in here
                        response = requests.post(self.URL1, json = data)
                        print(response.text) #this is the response text, should say it was successful in here 


                        #this is for notifying users of response taken, yes is for escalation
                        data = {'homeID': Constant.ACCOUNT_ID, 'resp': 'panic'}
                        #response holds the string returned from POST, if there was an error it should be in here
                        response = requests.post(self.URL2, json = data)
                        print("PANIC RESONSE: ",response.text) #this is the response text, should say it was successful in here
                        # stop beep
                        # play siren
                
                print("MessageHandler giving up lock end of loop")
                #self.shared_resources.q_lock.release()
          


"""

#this is for auto-escalation
URL = "https://jlt49k4n90.execute-api.us-east-2.amazonaws.com/beta/auto-escalate/"
data = {'homeID': Constant.ACCOUNT_ID}
#response holds the string returned from POST, if there was an error it should be in here
response = requests.post(url = URL, json = data)
responseText = response.text #this is the response text, should say it was successful in here
"""