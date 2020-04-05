#!usr/bin/python3

from sensor_interface import sensor_interface
import os
import RPi.GPIO as GPIO
import time
from ultra_proc import UltraProc

class Ultrasonic(sensor_interface):
    frequency = None
    duration = None
    isActive = False
    duration = None
    frequency = None
    num_channels = 1

    #set GPIO Pins
    GPIO_TRIGGER = 7
    GPIO_ECHO = 11

    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
        
        # set Trigger after 0.01ms to LOW
        time.sleep(.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()
        
        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
            
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
        
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
 
        return distance
    
    def initiate(self, response_list, outPath):
        start = time.time()
        print(response_list)
        list_lock, barrier, anomaly_dict, instance_id, acc_id, bucket_name = response_list[0]

        outfiles = []
        outfiles.append(outPath + 'ultra.txt')
        
        self.isActive = True
        print('Recording Distance...')

        output = ""
        total_time = 0
        try:
            while total_time < self.duration:
                dist = self.distance()
                output += str(dist) + "\n"
                time.sleep(self.frequency)
                total_time += self.frequency

            with open(outfiles[0], 'w') as outfile:
                outfile.write(output)
                
        except:
            print('Recording Failed')
            raise
        finally:
            print('cleaning gpio')
            GPIO.cleanup()
            self.isActive = False

        # check if anomaly in ultra data
        print('Ultrasonic anomaly detection')
        ultraProc = UltraProc()
        isAnomaly = ultraProc.isAnomaly(files)
        anomaly_dict['ultra'] = isAnomaly
        
        # wait until every thread has processed their files
        barrier.wait()
        print('ultra passed barrier')

        # check if any anomalies detected
        wasAnom = False
        for anomaly in anomaly_dict.values():
            if(anomaly):
                wasAnom = True
                break

        # list of objects
        obj_list = []
        if(wasAnom):
            client = S3_Client()
            # upload to s3
            for file_a in files:
                object_name = file_a.split('/')[-1]
                object_name = str(acc_id) + "/" + instance_id + '/' + 'ultrasonic' + '/' + object_name
                obj_list.append(object_name)
                client.upload_file(file_a, bucket_name, object_name)

        print('acquiring lock')
        with list_lock:
            response_list.append((obj_list, "ultrasonic"))
        
        end = time.time()
        print("Total ultra time to execute : [" + str(end - start) + "]")

            
    def connect(self):
        print('Connecting to Ultra')
        
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BOARD)
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
    
    def test(self):
        print('Testing Ultra')
        pass

    def __init__(self, duration, frequency):
        self.duration = duration
        self.frequency = frequency

