import threading
import os

from IncidentData import IncidentData
from run_sensors import run_everything
from Constant import Constant
import pickle
import ast
import sys


class LogicHandlerThread(threading.Thread):

    def __init__(self, shared_resources):
        threading.Thread.__init__(self)
        self.shared_resources = shared_resources    # get lock for shared resource is_armed

        def run(self):
            while True:

                panic = False
                record_incident = False  # DOES THIS NEED TO BE THE LINE BELOW ?
                #self.shared_resources.record_incident = False
                
                self.shared_resources.q_lock.acquire()  # get lock for shared resource is_armed

                if self.shared_resources.is_armed is True and self.shared_resources.is_active_alert is False:
                    ret_dict = None
                    r, w = os.pipe()
                    pid = os.fork()
                    if pid > 0:
                        os.close(w)
                        r = os.fdopen(r)
                        ret_dict = ast.literal_eval(r.read())
    
                        # parent process
                        print('Parent done waiting')
                        print("PARENT RET DICT : " + str(ret_dict))
    
                    else:
                        print('child running everything')
                        os.close(r)
                        # child process
                        ret_dict = run_everything(11)
                        w = os.fdopen(w, 'w')
                        w.write(str(ret_dict))
                        w.close()
    
                        print("CHILD RET DICT : " + str(ret_dict))
                        sys.exit(0)
    
                    print('RET DICT FINAL : ' + str(ret_dict))
    
                    if ret_dict["wasAlert"] is True:  # reduce time holding lock
                        record_incident = True     # should this be the line below?
                        #self.shared_resources.record_incident = True
                        self.shared_resources.is_active_alert = True
                        self.shared_resources.was_alert = True
                        print("\tLogicHandlerThread:\tSet Resource: Is Active Alert", self.shared_resources.is_active_alert)
                        print("\tLogicHandlerThread:\tSet Resource: Was Alert", self.shared_resources.was_alert)
                        if ret_dict["face_match_flag"] is False:  # is no face match a high alert or a self escalating one???
                            print("\LogicHandlerthread:\t the face match flag is ",ret_dict[face_match_flag])
                            #self.shared_resorces.is_max_alert = True

                elif self.shared_resources.is_panic is True:
                    ret_dict = None
                    r, w = os.pipe()
                    pid = os.fork()
                    if pid > 0:
                        os.close(w)
                        r = os.fdopen(r)
                        ret_dict = ast.literal_eval(r.read())

                        # parent process
                        print('Parent done waiting')
                        print("PARENT RET DICT : " + str(ret_dict))

                    else:
                        print('child running everything')
                        os.close(r)
                        # child process
                        ret_dict = run_everything(11)
                        w = os.fdopen(w, 'w')
                        w.write(str(ret_dict))
                        w.close()

                        print("CHILD RET DICT : " + str(ret_dict))
                        sys.exit(0)

                    print('RET DICT FINAL : ' + str(ret_dict))

                    record_incident = True
                    panic = True
                    print("\tLogicHandlerThread:\tCollected Data for Panic")
                    self.shared_resources.was_alert = True
                    print("\tLogicHandlerThread:\tSet Resource: Was Alert", self.shared_resources.was_alert)


                self.shared_resources.q_lock.release()  # release lock
            
                if record_incident is True:
                    incident_id = str(ret_dict["instance_id"])
                    face_match_flag = str(ret_dict["face_match_flag"])
                    image_path = ret_dict["camera"]
                    mic_path = ret_dict["mic"][0]
                    ultrasonic_path = ret_dict["ultrasonic"][0]
                    temp = IncidentData(Constant.ACCOUNT_ID, incident_id, face_match_flag, image_path, mic_path,
                                        ultrasonic_path)  # create incident data
                    self.shared_resources.db_conn.connection = self.shared_resources.db_conn.connect()  # connect
                    print(self.shared_resources.db_conn.insert_incident_data(temp))  # send to db and print

                    # self.shared_resources.db_conn.disconnect()  # disconnect is handled in dbConn

                    
"""                  
    def run(self):
        while True:
            record_incident = False
            self.shared_resources.q_lock.acquire()  # get lock for shared resource is_armed
            if self.shared_resources.is_armed is True:

        if self.shared_resources.is_armed is True and self.shared_resources.is_ongoing_threat is False:
                ret_dict = run_everything(11)
                if ret_dict["wasAlert"] is True:  # reduce time holding lock
                    self.shared_resources.record_incident = True
                    self.shared_resources.was_alert = True
            self.shared_resources.q_lock.release()  # release lock
            if self.shared_resources.record_incident is True and self.shared_resources.is_ongoing_threat is False:
                incident_id = str(ret_dict["instance_id"])
                face_match_flag = str(ret_dict["face_match_flag"])
                image_path = ret_dict["camera"]
                mic_path = ret_dict["mic"][0]
                ultrasonic_path = ret_dict["ultrasonic"][0]
                temp = IncidentData(Constant.ACCOUNT_ID, incident_id, face_match_flag, image_path, mic_path,
                                    ultrasonic_path)  # create incident data
                self.shared_resources.db_conn.connection = self.shared_resources.db_conn.connect()  # connect
                print(self.shared_resources.db_conn.insert_incident_data(temp))  # send to db and print
                self.shared_resources.is_ongoing_threat = True
                self.shared_resources.record_incident = False
"""    
