#!usr/bin/python3

from sensor_interface import sensor_interface
from picamera import PiCamera
from time import sleep
import os
import time
from cam_proc import CamProc
from s3_client import S3_Client

class Camera(sensor_interface):
    camera = None
    isActive = None
    duration = None
    frequency = None

    def initiate(self, response_list, outPath):
        start = time.time()
        print(response_list)
        list_lock, barrier, anomaly_dict, instance_id, acc_id, bucket_name = response_list[0]

        outfiles = []
        try:
            self.isActive = True
            #self.camera.start_preview()
            print('Initiating Camera')
            for i in range(self.duration):
                cur_path = outPath + 'image_' + str(i) + '.jpg'
                outfiles.append(cur_path)
                
                print('\tCapturing [' + str(i) + ']')

                self.camera.capture(cur_path)
                sleep(self.frequency)

            #self.camera.stop_preview()
        except:
            print('Camera Failed')
        finally:
            print('--------------- INITIATE CAM : ' + str(self.camera))
            self.camera.close()
            self.isActive = False

        # get user faces
        user_files = self.get_user_faces(acc_id, bucket_name)

        image_dict = {}
        image_dict['users'] = user_files
        image_dict['sampled'] = outfiles
        # check if anomaly in cam data
        print('camera anomaly detection')
        camProc = CamProc()
        isAnomaly, face_match = camProc.isAnomaly(image_dict)
        anomaly_dict['cam'] = isAnomaly
        anomaly_dict['face'] = face_match
        print('CAM ANOM : ' + str(isAnomaly))
        
        print("barrier in cam: ",barrier)
       # wait until every thread has processed their files
        barrier.wait()
        print('cam passed barrier')

        # check if any anomalies detected
        wasAnom = False
        for key,anomaly in zip(anomaly_dict.keys(),anomaly_dict.values()):
            if key == 'face':
                continue
            if(anomaly):
                wasAnom = True
                break
        #if anomaly_dict['face']:
        #    wasAnom = False
        # list of objects
        obj_list = []

        # upload to s3 on anomaly
        if(wasAnom):
                  
            client = S3_Client()
            # upload to s3
            for file_a in outfiles:
                object_name = file_a.split('/')[-1]
                object_name = str(acc_id) + "/" + str(instance_id) + '/' + 'camera' + '/' + object_name
                obj_list.append(object_name)
                client.upload_file(file_a, bucket_name, object_name)

        print('acquiring lock')
        with list_lock:
            response_list.append((obj_list, "camera"))

        end = time.time()
        print("Total cam time to execute : [" + str(end - start) + "]")

    def get_user_faces(self, acc_id, bucket_name):
        client = S3_Client()
        files = client.get_user_face_files(bucket_name, acc_id)
        return files
        
    def connect(self):
        print('Camera Connecting')
        try:
            self.camera = PiCamera()
            # Take out this if no rotation is needed
            #self.camera.rotation = 180
            self.isActive = True
            print('Cam success')
        except:
            print("camera error")
        print('--------------- CONNECT CAM : ' + str(self.camera))

        return True
    
    def test(self):
        pass

    def __init__(self, duration, frequency):
        self.duration = duration
        self.frequency = frequency
        self.isActive = False
