#!usr/bin/python3

from sensor_interface import sensor_interface
from picamera import PiCamera
from time import sleep
import os
import time

class Camera(sensor_interface):
    camera = None
    isActive = None
    duration = None
    frequency = None

    def initiate(self, response_list, outPath):
        start = time.time()
        print(response_list)
        list_lock = response_list[0]
        
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
            self.isActive = False

        print('Camera locking')
        with list_lock:
            print('Camera locked')

            response_list.append((outfiles, "camera"))
            print('Camera added to list')
            
        end = time.time()
        print("Total camera time to execute : [" + str(end - start) + "]")

            
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

