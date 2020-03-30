from picamera import PiCamera
from time import sleep

camera = PiCamera()

# Take out this if no rotation is needed
# camera.rotation = 180

camera.start_preview()
sleep(5)

# This code takes the picture
for i in range(10):
    camera.capture('./data/cam/charles_' + str(i) + '.jpg')
    sleep(1)

camera.stop_preview()
