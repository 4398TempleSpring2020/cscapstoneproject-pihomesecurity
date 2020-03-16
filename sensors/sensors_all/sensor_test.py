#!usr/bin/python3
from sensor_manager import Sensor_Manager
from microphone import Microphone

if __name__ == '__main__':
    sm = Sensor_Manager()
    sm.add_sensor(Microphone(duration=10, frequency=44100))
    sm.connect_all()
    sm.initiate_all()