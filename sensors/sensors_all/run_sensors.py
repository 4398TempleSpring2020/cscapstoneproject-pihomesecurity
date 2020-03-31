#!usr/bin/python3
from sensor_manager import Sensor_Manager
from microphone import Microphone
from camera import Camera
from ultrasonic import Ultrasonic
from ultra_proc import UltraProc
from mic_proc import MicProc
from cam_proc import CamProc
from s3_client import s3_client
import time

def run_sensors(duration):
    sm = Sensor_Manager() # takes in acc iD
    sm.add_sensor(Microphone(duration=duration, frequency=44100))
    sm.add_sensor(Camera(duration=duration, frequency=.5))
    sm.add_sensor(Ultrasonic(duration=duration, frequency=.1))
    sm.connect_all()
    ret_list = sm.initiate_all()

    return ret_list
    
    
def run_everything(acc_id):
    '''
    Handles upload of detection files to S3
    Preprocesses sensor data
    Triggers camera
    continuously records mic and ultra in background
    lock itself on data trigger return, waits for signal from server to start again
    '''
    ret_list = run_sensors(10)

    print('------------ Sensors Complete -----------------')
    for item in ret_list:
        print(item)
    print('------------ Data Acquired -----------------')
    print('------------ Processing Data -----------------')

    micProc = MicProc()
    ultraProc = UltraProc()
    camProc = CamProc()
    
    for files, src in ret_list:
        if(src == 'camera'):
            print('Camera Data')
            camProc.test_cv()
        elif(src == 'microphone'):
            print('Microphone Data')
            mic_signals, mic_names = micProc.get_files(files)
            #micProc.plot_signals(mic_signals, mic_names, "Microphone Signals")
            #micProc.plot_each_signals(mic_signals, mic_names, "Individual Microphone Signals")
        elif(src == 'ultrasonic'):
            print('Ultrasonic Data')
            ultra_signals, ultra_names = ultraProc.get_files(files)
            #ultraProc.plot_signals(ultra_signals, ultra_names, "Ultrasonic Sensor Signals")
            #ultraProc.plot_each_signals(ultra_signals, ultra_names,
            #                            "Individual Ultrasonic Sensor Signals")
        else:
            print('Error: Invalid label : [' + str(src) + ']')
            
    print('------------ Data Processed -----------------')
    
    print('------------ Uploading to S3 -----------------')

    ret_dict = {}
    client = s3_client()
    bucket_name = 'whateverworks'
    instance_id = str(time.time())
    for files, src in ret_list:
        obj_list = []
        for file_a in files:
            object_name = file_a.split('/')[-1]
            object_name = str(acc_id) + "/" + instance_id + '/' + src + '/' + object_name
            obj_list.append(object_name)
            client.upload_file(file_a, bucket_name, object_name)
        print(src)
        print(obj_list)
        ret_dict[src] = obj_list
    ret_dict['bucket'] = bucket_name
    ret_dict['instance_id'] = instance_id
    ret_dict['face_match_flag'] = False
    ret_dict['wasAlert'] = False
    ret_dict['trigger_sensor_type'] = []
    
    print('------------ Upload Complete -----------------')

    print(ret_dict)

    return(ret_dict)
    # (ultra_bucket_filename[], mic_bucket_filename[], cam_bucket_filename[],
    # trigger_sensor_type, face_match_flag, incident_id, wasAlert

    '''
    # executed on a thread
    while isArmed:
        acquire soundlock
        # block 10 seconds
        data = run_lukes_sensor_script()
        
        if(wasAlert):
            sound_alarm() -> while true: acuire SL 
                                                   if ShouldContinue: soundAlarm
                                                   else: quit
                                         release SL

        if(incoming_user_message > 0):
            for message in user_messages:
                handle(message) -> one of these should modify shouldContinue
        release soundLock
    '''
