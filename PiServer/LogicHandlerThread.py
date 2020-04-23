import threading
import os
import time

from IncidentData import IncidentData
from run_sensors import run_everything
from Constant import Constant
import pickle
import ast
import sys
from pprint import pprint
from TimerCountdownThread import TimerCountdownThread
import requests
from subprocess import Popen

class LogicHandlerThread(threading.Thread):

    def __init__(self, shared_resources):
        threading.Thread.__init__(self)
        self.shared_resources = shared_resources    # get lock for shared resource is_armed
        self.URL = "https://jlt49k4n90.execute-api.us-east-2.amazonaws.com/beta/incident-alert/"

    def run(self):
        #printCt = 0
        print("Logic Handler running")
        while True:
         
            #if printCt%30 ==0:
                #print("Logic Handler Thread running")
         
            panic = False
            record_incident = False  # DOES THIS NEED TO BE THE LINE BELOW ?
            
            self.shared_resources.q_lock.acquire()  # get lock for shared resource is_armed
            #sound = Popen(["aplay", Constant.CHIME])
            #self.shared_resources.sound_pid= sound.pid
            #time.sleep(5)
            #sound.kill()
            #self.shared_resources.sound_pid.terminate()
            #if printCt%30 ==0:
                #print("Logic Handler Aquired Lock")   
            if self.shared_resources.is_armed is True:
                
                if self.shared_resources.is_active_incident is False:
                    print("Logic Handler has lock, is Armed,is not active incident")
                    ret_dict = None
                    r, w = os.pipe()
                    pid = os.fork()
                    if pid > 0:
                        os.close(w)
                        r = os.fdopen(r)
                        ret_dict = ast.literal_eval(r.read())
    
                        # parent process
                        print('Parent done waiting')
                        pprint("PARENT RET DICT : " + str(ret_dict))
    
                    else:
                        print('child running everything')
                        os.close(r)
                        # child process
                        ret_dict = run_everything(11)
                        w = os.fdopen(w, 'w')
                        w.write(str(ret_dict))
                        w.close()
    
                        pprint("CHILD RET DICT : " + str(ret_dict))
                        sys.exit(0)
                        print("***************child should have died***********")
                        
                    
                    pprint('RET DICT FINAL : ' + str(ret_dict))
    
                    if ret_dict["wasAlert"] is True:  # reduce time holding lock
                        #self.shared_resources.q_lock.acquire()
                        #print("Logic Handler acquired lock for alert detected")
                        record_incident = True     # should this be the line below?
                        #self.shared_resources.record_incident = True
                        if ret_dict["face_match_flag"] is False:  # is no face match a high alert or a self escalating one???
                            print("\LogicHandlerthread:\t the face match flag is ",ret_dict["face_match_flag"])
                            self.shared_resources.is_active_incident = True
                            self.shared_resources.was_alert = True
                            print("\tLogicHandlerThread:\tSet Resource: Is Active Incident", self.shared_resources.is_active_incident)
                            print("\tLogicHandlerThread:\tSet Resource: Was Alert", self.shared_resources.was_alert)
                        elif ret_dict["face_match_flag"] is True:
                            print("\LogicHandlerthread:\t the face match flag is ",ret_dict["face_match_flag"])
                            self.shared_resources.is_active_incident = False
                            print("\tLogicHandlerThread:\tSet Resource: Is Active Incident", self.shared_resources.is_active_incident)

                        print("Logic Handler released lock after normal workflow")


            elif self.shared_resources.is_panic is True:
                if self.shared_resources.is_active_incident is False:
                    ret_dict = None
                    r, w = os.pipe()
                    pid = os.fork()
                    if pid > 0:
                        os.close(w)
                        r = os.fdopen(r)
                        ret_dict = ast.literal_eval(r.read())

                        # parent process
                        print('Parent done waiting')
                        pprint("PARENT RET DICT : " + str(ret_dict))

                    else:
                        print('child running everything')
                        os.close(r)
                        # child process
                        ret_dict = run_everything(11)
                        w = os.fdopen(w, 'w')
                        w.write(str(ret_dict))
                        w.close()

                        pprint("CHILD RET DICT : " + str(ret_dict))
                        sys.exit(0)

                    pprint('RET DICT FINAL : ' + str(ret_dict))

                    record_incident = True
                    panic = True
                    print("\tLogicHandlerThread:\tCollected Data for Panic")
                    self.shared_resources.was_alert = True
                    self.shared_resources.is_active_incident = True
                    print("\tLogicHandlerThread:\tSet Resource: Was Alert", self.shared_resources.was_alert)
                    print("\tLogicHandlerThread:\tSet Resource: Is Active Alert", self.shared_resources.is_active_incident)
            
       
            self.shared_resources.q_lock.release()  # release lock
            #if printCt%10 ==0:
            #print("Logic Handler released lock")
            
            if record_incident is True:
                print("recording incident in database")
                incident_id = str(ret_dict["instance_id"])
                if ret_dict["face_match_flag"] == True:
                    face_match_flag = 1
                else:
                    face_match_flag = 0
                if ret_dict["face_match_flag"] == False and panic == False and self.shared_resources.is_active_incident==True:
                    
                #*************************
                #basecmd = ["mplayer", "-ao", "alsa:device=bluetooth"]
                    
                    sound = Popen(["aplay", Constant.CHIMESIREN])
                    self.shared_resources.sound_pid = sound.pid
                    
                    data = {'homeID': Constant.ACCOUNT_ID, 'incidentID': incident_id, 'type': "anomaly"}
                    #response holds the string returned from POST, if there was an error it should be in here
                    response = requests.post(self.URL, json = data)
                    print("INCIDENT ALERT RESONSE: ",response.text) #this is the response text, should say it was successful in here
                    #timer_thread = TimerCountdownThread(self.shared_resources)
                    #timer_thread.start()
                    #print("Timer has started for receiving responses")
                elif panic==True:
                    data = {'homeID': Constant.ACCOUNT_ID, 'incidentID': incident_id, 'type': "panic"}
                    #response holds the string returned from POST, if there was an error it should be in here
                    response = requests.post(self.URL, json = data)
                    print("PANIC ALERT RESONSE: ",response.text) #this is the response text, should say it was successful in here
                    
                image_path = ret_dict["camera"]
                mic_path = ret_dict["mic"][0]
                ultrasonic_path = ret_dict["ultrasonic"][0]
                temp = IncidentData(Constant.ACCOUNT_ID, incident_id, face_match_flag, image_path, mic_path,
                                    ultrasonic_path)  # create incident data
                self.shared_resources.db_conn.connection = self.shared_resources.db_conn.connect()  # connect
                pprint(self.shared_resources.db_conn.insert_incident_data(temp))  # send to db and print

                # self.shared_resources.db_conn.disconnect()  # disconnect is handled in dbConn
            #printCt = printCt +1
                    