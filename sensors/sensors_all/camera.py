#!usr/bin/python3

from sensor_interface import sensor_interface
from picamera import *
from time import sleep
import os

class Camera(sensor_interface):
    camera
    isActive
    duration
    frequency

    def initiate(self):
        if this.isActive:
            print('Initiating Camera')
            path = os.getcwd()

            count = floor(frequency * duration)
            rest = floor(1000/count)
            for i in range(count):
                cur_path = path + 'image_' + str(i) + '.jpg'
                print('\tCapturing [' + cur_path + ']')
                camera.capture(cur_path)
                sleep(rest)
            return True
        else:
            print('Camera Failed')
            return False
    
    def connect(self):
        try:
            print('Camera Connecting')
            this.camera = PiCamera()
            # Take out this if no rotation is needed
            camera.rotation = 180
            this.isActive = True
        except picamera.PiCameraError:
            print('Camera Error')
            raise
    
    def test(self):
        pass

    def __init__(self, duration, frequency):
        this.duration = duration
        this.frequency = frequency
        this.isActive = False
        pass
