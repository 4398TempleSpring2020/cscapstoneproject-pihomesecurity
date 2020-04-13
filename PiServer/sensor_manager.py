from camera import Camera
from microphone import Microphone
import threading
import time
import os

class Sensor_Manager():
    sensors = []

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def connect_all(self):
        for sensor in self.sensors:
            sensor.connect()

    def initiate_all(self, acc_id, bucket_name):
        # store thread output files
        ret_list = []
        list_lock = threading.Lock()
        # create a barrier to wait for all sensors
        barrier = threading.Barrier(len(self.sensors))
        anomaly_dict = {}
        anomaly_dict['mic'] = False
        anomaly_dict['ultra'] = False
        anomaly_dict['cam'] = False

        instance_id = time.time()
        ret_list.append([list_lock, barrier, anomaly_dict, instance_id, acc_id, bucket_name])

        # list of threads
        thread_list = []

        # for each sensor, create a thread
        for sensor in self.sensors:
            t = threading.Thread(target=self.run_sensor, args=(sensor, ret_list))
            thread_list.append(t)
            t.start()

        # wait for all threads to finish
        for thread_a in thread_list:
            thread_a.join()

        # return object list and meta data
        return(ret_list[1:], anomaly_dict, instance_id, acc_id)
    
    def run_sensor(self, sensor, ret_list):
        sensor.initiate(ret_list, "./")

    def test_all(self):
        for sensor in self.sensors:
            sensor.test()
