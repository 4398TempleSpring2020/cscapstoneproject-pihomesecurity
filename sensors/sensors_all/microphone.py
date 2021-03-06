#!usr/bin/python3

from sensor_interface import sensor_interface
import sounddevice as sd
import os
import soundfile as sf
import time

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
        list_lock = response_list[0]

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

        with list_lock:
            response_list.append((outfiles, "microphone"))

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
