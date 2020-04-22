#!usr/bin/python3

from sensor_interface import sensor_interface
import sounddevice as sd
import os
import soundfile as sf
import time
from mic_proc import MicProc
from s3_client import S3_Client

class Microphone(sensor_interface):
    frequency = None
    duration = None
    isActive = False
    duration = None
    frequency = None
    num_channels = 1
    
    def initiate(self, response_list, outPath):
        start = time.time()
        print(response_list)
        list_lock, barrier, anomaly_dict, instance_id, acc_id, bucket_name = response_list[0]

        outfiles = []
        outfiles.append(outPath + 'audio.wav')
        
        self.isActive = True
        print('Recording Audio...')
        try:
            myrecording = sd.rec(int(self.duration * self.frequency), samplerate=self.frequency, channels=self.num_channels)
            sd.wait()
            print("Recording Complete")

            sf.write(outfiles[0], myrecording, self.frequency)
        except:
            print('Recording Failed')
            raise
        finally:
            self.isActive = False

        # check if anomaly in ultra data
        print('microphone anomaly detection')
        micProc = MicProc()
        isAnomaly = micProc.isAnomaly(outfiles)
        anomaly_dict['mic'] = isAnomaly
        print('MIC ANOM : ' + str(isAnomaly))
        print("barrier in mic: ", barrier)
        # wait until every thread has processed their files
        barrier.wait()
        print('mic passed barrier')

        # check if any anomalies detected
        wasAnom = False
        for key,anomaly in zip(anomaly_dict.keys(),anomaly_dict.values()):
            if key == 'face':
                continue
            if(anomaly):
                wasAnom = True
                break
            
        if anomaly_dict['face']:
            wasAnom = False

      
        # list of objects
        obj_list = []
        if(wasAnom):
            client = S3_Client()
            # upload to s3
            for file_a in outfiles:
                object_name = file_a.split('/')[-1]
                object_name = str(acc_id) + "/" + str(instance_id) + '/' + 'microphone' + '/' + object_name
                obj_list.append(object_name)
                client.upload_file(file_a, bucket_name, object_name)

        print('acquiring lock')
        with list_lock:
            response_list.append((obj_list, "mic"))
        
        end = time.time()
        print("Total mic time to execute : [" + str(end - start) + "]")
            
    def connect(self):
        print('Connecting to Microphone')
        pass
    
    def test(self):
        print('Testing Microphone')
        pass

    def __init__(self, duration, frequency):
        self.duration = duration
        self.frequency = frequency
