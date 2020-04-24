#!usr/bin/python3
from sensor_manager import Sensor_Manager
from microphone import Microphone
from camera import Camera
from ultra_proc import UltraProc
from mic_proc import MicProc
from cam_proc import CamProc
import os
import unittest
from run_sensors import run_sensors
from camera_proc_help import facial_recognition
from s3_client import S3_Client
from picamera import PiCamera
from time import sleep
import sounddevice as sd
import soundfile as sf


class TestSensors(unittest.TestCase):
    # ensure running sensors returns a tuple with 4 items, each containing non null information
    def test_running_sensors(self):
        print('testing running all sensors')
        bucket_name = "mypishield"
        acc_old_id = 11

        # run all sensorsls
        ret_vals = run_sensors(10, acc_old_id, bucket_name)

        # check length
        self.assertEqual(len(ret_vals), 4)        

        # unpack it and check existance
        ret_list, anomaly_dict, instance_id, acc_id = ret_vals
        self.assertTrue(not ret_list is None)
        self.assertTrue(not anomaly_dict is None)
        self.assertEqual(len(anomaly_dict), 4)
        self.assertTrue(not instance_id is None)
        self.assertTrue(acc_id == acc_old_id)
        
    # test image processing script for known output (hostile / friendly)
    def test_image_proc_all(self):
        print('Testing image processing')
        known = ['./known_people/cat.jpg',
                 './known_people/charles.jpg', './known_people/luke.jpg']
        # true
        isAnom, face_match = facial_recognition(["unknown_people/unknown1.jpg"], known)
        self.assertTrue(isAnom)
        self.assertTrue(face_match)

        print("Isanom " + str(isAnom) + " face match " + str(face_match))
        isAnom, face_match = facial_recognition(["unknown_people/unknown2.jpg"], known)
        print("Isanom " + str(isAnom) + " face match " + str(face_match))

        # true, true
        self.assertTrue(isAnom)
        self.assertTrue(face_match)
        
        isAnom, face_match = facial_recognition(["unknown_people/unknown3.jpg"], known)
        print("Isanom " + str(isAnom) + " face match " + str(face_match))

        # false, true
        self.assertTrue(isAnom)
        self.assertFalse(face_match)
        
        isAnom, face_match = facial_recognition(["unknown_people/unknown4.jpg"], known)
        print("Isanom " + str(isAnom) + " face match " + str(face_match))

        # true, true
        self.assertTrue(isAnom)
        self.assertTrue(face_match)
 
    # test that we recognize far anomalies for ultra
    def test_ultra_proc_far(self):
        print('Testing ultra processing far')

        ultraProc = UltraProc()
        fname = ["./data/ultra/far_anomaly.txt"]
        isAnom = ultraProc.isAnomaly(fname)

        self.assertEqual(isAnom, True)

    # test that we recognize medium anomalies for ultra
    def test_ultra_proc_med(self):
        print('Testing ultra processing med')

        ultraProc = UltraProc()
        fname = ["./data/ultra/medium_anomaly.txt"]
        isAnom = ultraProc.isAnomaly(fname)

        self.assertEqual(isAnom, True)

    # test that we recognize close anomalies for ultra
    def test_ultra_proc_close(self):
        print('Testing ultra processing close')

        ultraProc = UltraProc()
        fname = ["./data/ultra/close_anomaly.txt"]
        isAnom = ultraProc.isAnomaly(fname)

        self.assertEqual(isAnom, True)

    # test that we do not recognize static anomalies for ultra
    def test_ultra_proc_static(self):
        print('Testing ultra processing static')

        ultraProc = UltraProc()
        fname = ["./data/ultra/static.txt"]
        isAnom = ultraProc.isAnomaly(fname)

        self.assertEqual(isAnom, False)

    # test that we do not recognize distant walking anomalies for ultra
    def test_ultra_proc_offscreen(self):
        print('Testing ultra processing offscreen')

        ultraProc = UltraProc()
        fname = ["./data/ultra/offscreenwalking.txt"]
        isAnom = ultraProc.isAnomaly(fname)

        self.assertEqual(isAnom, False)

    # test that we recognize close anomalies for mic
    def test_mic_proc_close(self):
        print('Testing mic processing close')

        micProc = MicProc()
        fname = ["./data/mic/close_talking.wav"]
        isAnom = micProc.isAnomaly(fname)

        self.assertEqual(isAnom, True)

    # test that we recognize loud clapping for mic
    def test_mic_proc_loud(self):
        print('Testing mic processing loud')

        micProc = MicProc()
        fname = ["./data/mic/loud_clapping.wav"]
        isAnom = micProc.isAnomaly(fname)

        self.assertEqual(isAnom, True)

    # test that we do not recognize silent fo mic
    def test_mic_proc_silent(self):
        print('Testing mic processing silent')

        micProc = MicProc()
        fname = ["./data/mic/silent.wav"]
        isAnom = micProc.isAnomaly(fname)

        self.assertEqual(isAnom, False)

    # test that each meta file exists after downloading faces
    def test_s3_user_face_download_meta(self):
        print('Testing s3 download meta')

        client = S3_Client()
        files = client.get_user_face_files("mypishield", 11)

        meta_files = []
        for file_a in files:
            meta_files.append(file_a.split('.')[:-1][0] + "_meta.txt")

        for mfile in meta_files:
            self.assertEqual(os.path.exists(mfile), True)

    # test that each face file exists after downloading faces
    def test_s3_user_face_download(self):
        print('Testing s3 download existence')

        client = S3_Client()
        files = client.get_user_face_files("mypishield", 11)

        for file_a in files:
            self.assertEqual(os.path.exists(file_a), True)

    # test that the camera can take a picture
    def test_cam_takes_pic(self):
        cam_file = './test_image.jpg'

        # delete file if it exists
        if os.path.exists(cam_file):
            os.remove(cam_file)

        # create a camera
        camera = PiCamera()
        
        # This code takes the picture
        camera.capture(cam_file)

        self.assertEqual(os.path.exists(cam_file), True)

    # ensures microphone can actually record sound
    def test_mic_records_audio(self):
        mic_file = './test_mic.wav'

        # delete file if it exists
        if os.path.exists(mic_file):
            os.remove(mic_file)

        # some defined constants
        duration = 60
        frequency = 44100

        # record audo
        try:
            # get recording
            myrecording = sd.rec(int(duration * frequency), samplerate=frequency, channels=1)
            sd.wait()

            # save recording
            sf.write(mic_file, myrecording, frequency)
        except:
            print('Recording Failed')

        # ensure file now exists
        self.assertEqual(os.path.exists(mic_file), True)

    # tests that we can connect to the ultrasonic sensor and record distance measurements
    def test_ultra_records_distance(self):
        ultra_file = './test_ultra.txt'

        # delete file if it exists
        if os.path.exists(ultra_file):
            os.remove(ultra_file)

        GPIO_TRIGGER = 12
        GPIO_ECHO = 18
        frequency = .1
        output = ""
        total_time = 0
        try:
            while total_time < 60:
                # set Trigger to HIGH
                GPIO.output(GPIO_TRIGGER, True)
        
                # set Trigger after 0.01ms to LOW
                time.sleep(.00001)
                GPIO.output(GPIO_TRIGGER, False)
                
                StartTime = time.time()
                StopTime = time.time()
        
                # save StartTime
                while GPIO.input(GPIO_ECHO) == 0:
                    StartTime = time.time()
            
                # save time of arrival
                while GPIO.input(GPIO_ECHO) == 1:
                    StopTime = time.time()
        
                # time difference between start and arrival
                TimeElapsed = StopTime - StartTime
                # multiply with the sonic speed (34300 cm/s)
                # and divide by 2, because there and back
                dist = (TimeElapsed * 34300) / 2

                if (dist>170):
                    continue
                elif (dist<0):
                    continue
                
                output += str(dist) + "\n"
            
                time.sleep(frequency)
                total_time += frequency

            with open(ultra_file, 'w') as outfile:
                outfile.write(output)
                
        except:
            print('Recording Failed')
        finally:
            GPIO.cleanup()

        # ensure file now exists
        self.assertEqual(os.path.exists(ultra_file), True)
            
if __name__ == '__main__':
    unittest.main()
