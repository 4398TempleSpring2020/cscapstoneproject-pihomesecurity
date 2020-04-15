#!usr/bin/python3
from sensor_manager import Sensor_Manager
from microphone import Microphone
from camera import Camera

if __name__ == '__main__':
    '''
    Handles upload of detection files to S3
    Preprocesses sensor data
    Triggers camera
    continuously records mic and ultra in background
    lock itself on data trigger return, waits for signal from server to start again
    '''

    sm = Sensor_Manager() # takes in acc iD
    sm.add_sensor(Microphone(duration=60, frequency=44100))
    sm.add_sensor(Camera(duration=60, frequency=1))
    sm.connect_all()
    sm.initiate_all()

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
