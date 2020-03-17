from picamera import PiCamera
from time import sleep

camera = PiCamera()

# Take out this if no rotation is needed
camera.rotation = 180

camera.start_preview()
sleep(5)

# This code takes the picture
camera.capture('/home/pi/cscapstoneproject-pihomesecurity/camera/image.jpg')
camera.stop_preview()
