#!usr/bin/python3

from sensor_interface import sensor_interface
from picamera import *
from time import sleep
import os

class Camera(sensor_interface):
    camera = None
    isActive = None
    duration = None
    frequency = None


    def initiate(self):
        if self.isActive:
            print('Initiating Camera')
            path = os.getcwd()

            count = int(self.frequency * self.duration)
            rest = int(1000/count)
            for i in range(count):
                cur_path = path + 'image_' + str(i) + '.jpg'
                print('\tCapturing [' + cur_path + ']')
                self.camera.capture(cur_path)
                sleep(rest)
            return True
        else:
            print('Camera Failed')
            return False
    
    def connect(self):
        try:
            print('Camera Connecting')
            self.camera = picamera.PiCamera()
            # Take out this if no rotation is needed
            camera.rotation = 180
            self.isActive = True
        except picamera.PiCameraError:
            print('Camera Error')
            raise
    
    def test(self):
        pass

    def __init__(self, duration, frequency):
        self.duration = duration
        self.frequency = frequency
        self.isActive = False
