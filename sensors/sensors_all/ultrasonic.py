#!usr/bin/python3

from sensor_interface import sensor_interface
import os
import RPi.GPIO as GPIO
import time

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
        time.sleep(self.frequency)
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
        print(response_list)
        list_lock = response_list[0]

        outfiles = []
        outfiles.append(outPath + 'ultra.txt')
        
        self.isActive = True
        print('Recording Distance...')

        total_time = 0
        try:
            with open(outfiles[0], 'w') as outfile:
                while total_time < self.duration:
                    dist = self.distance()
                    outfile.write(str(dist) + "\n")
                    
                    time.sleep(self.frequency)
                    total_time += self.frequency
        except:
            print('Recording Failed')
            raise
        finally:
            GPIO.cleanup()
            self.isActive = False

        with list_lock:
            response_list.append((outfiles, "microphone"))
            
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

