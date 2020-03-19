#from camera import Camera
#from microphone import Microphone

class Sensor_Manager():
    sensors = []

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def connect_all(self):
        for sensor in self.sensors:
            sensor.connect()

    def initiate_all(self):
        for sensor in self.sensors:
            sensor.initiate()

    def test_all(self):
        for sensor in self.sensors:
            sensor.test()