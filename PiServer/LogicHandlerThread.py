import threading

from IncidentData import IncidentData
from run_sensors import run_everything
from Constant import Constant


class LogicHandlerThread(threading.Thread):

    def __init__(self, shared_resources):
        threading.Thread.__init__(self)
        self.shared_resources = shared_resources
        
    def run(self):
        while True:
            record_incident = False
            self.shared_resources.q_lock.acquire()  # get lock for shared resource is_armed
            if self.shared_resources.is_armed is True:
                ret_dict = run_everything(11)

                # create pipe
                # fork
                # if child:
                #     ret_dict = run_everything
                #     send data over pipe
                #     exit()
                # if parent:
                #     wait to receive entire ret dict over pip
                # parent can now continue on as normal
                
                if ret_dict["wasAlert"] is True:  # reduce time holding lock
                    record_incident = True
                    self.shared_resources.is_ongoing_threat = True
                    self.shared_resources.was_alert = True
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
                # log to text file
                #self.shared_resources.db_conn.disconnect()  # disconnect
