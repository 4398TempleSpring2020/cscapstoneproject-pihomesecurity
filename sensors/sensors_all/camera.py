#!usr/bin/python3

from sensor_interface import sensor_interface
from picamera import PiCamera
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
            for i in range(self.duration):
                cur_path = './image_' + str(i) + '.jpg'
                print('\tCapturing [' + cur_path + ']')
                self.camera.capture(cur_path)
                sleep(1)
            return True
        else:
            print('Camera Failed')
            return False
    
    def connect(self):
        print('Camera Connecting')
        try:
            self.camera = PiCamera()
            # Take out this if no rotation is needed
            self.camera.rotation = 180
            self.isActive = True
            return True
        except:
            print("camera error")
            return False
    
    def test(self):
        pass

    def __init__(self, duration, frequency):
        self.duration = duration
        self.frequency = frequency
        self.isActive = False
