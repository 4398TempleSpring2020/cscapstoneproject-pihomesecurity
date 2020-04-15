#!usr/bin/python3
from sensor_manager import Sensor_Manager
from microphone import Microphone
from camera import Camera
from ultrasonic import Ultrasonic
from ultra_proc import UltraProc
from mic_proc import MicProc
from cam_proc import CamProc
from s3_client import S3_Client
import time

def run_sensors(duration, acc_id, bucket_name):
    sm = Sensor_Manager() # takes in acc iD
    sm.add_sensor(Microphone(duration=duration, frequency=44100))
    sm.add_sensor(Camera(duration=duration, frequency=.5))
    sm.add_sensor(Ultrasonic(duration=duration, frequency=.1))
    sm.connect_all()
    return(sm.initiate_all(acc_id, bucket_name))
    
def run_everything(acc_id):
    '''
    Handles upload of detection files to S3
    Preprocesses sensor data
    Triggers camera
    continuously records mic and ultra in background
    lock itself on data trigger return, waits for signal from server to start again
    '''
    bucket_name = "mypishield"

    print('-------------- RUNNING SENSORS ---------------------')
    ret_list, anomaly_dict, instance_id, acc_id = run_sensors(10, acc_id, bucket_name)

    print('------------ Sensors Complete -----------------')
    for item in ret_list:
        print(item)

    print (anomaly_dict)
    print(instance_id)
    print(acc_id)
    
    print('------------ Data Acquired -----------------')

    print('------------ CONSTRUCTING RESPONSE -----------------')

    wasAlert = False
    trig_type = []
    for sensor_type in anomaly_dict:
        was_triggered = anomaly_dict[sensor_type]
        if was_triggered:
            wasAlert = True
            trig_type.append(sensor_type)
            
    ret_dict = {}
    for files, src in ret_list:
        ret_dict[src] = files

    ret_dict['bucket'] = bucket_name
    ret_dict['instance_id'] = instance_id
    ret_dict['face_match_flag'] = False
    ret_dict['wasAlert'] = wasAlert
    ret_dict['trigger_sensor_type'] = trig_type
    
    print('------------ RESPONSE CONSTRUCTED -----------------')

    print(ret_dict)

    return(ret_dict)
    # (ultra_bucket_filename[], mic_bucket_filename[], cam_bucket_filename[],
    # trigger_sensor_type, face_match_flag, incident_id, wasAlert
