#!usr/bin/python3

from sensor_interface import sensor_interface
import sounddevice as sd
import os
import soundfile as sf

class Microphone(sensor_interface):
    frequency = None
    duration = None
    isActive = False
    duration = None
    frequency = None
    num_channels = 1
    
    def initiate(self):
        self.isActive = True
        print('Recording Audio...')
        try:
            myrecording = sd.rec(int(self.duration * self.frequency), samplerate=self.frequency, channels=self.num_channels)
            sd.wait()
            print("Recording Complete")

            sf.write('./audio.wav', myrecording, self.frequency)
        except:
            print('Recording Failed')
            raise
        finally:
            self.isActive = False
    
    def connect(self):
        print('Connecting to Microphone')
        pass
    
    def test(self):
        print('Testing Microphone')
        pass

    def __init__(self, duration, frequency):
        self.duration = duration
        self.frequency = frequency
