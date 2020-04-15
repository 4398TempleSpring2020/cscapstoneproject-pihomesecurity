import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.start_recording('test.h264')
    camera.rotation = 180
    camera.start_preview()
    camera.wait_recording(10)   #This is how many seconds the camera records
    camera.stop_recording()
    camera.stop_preview()

