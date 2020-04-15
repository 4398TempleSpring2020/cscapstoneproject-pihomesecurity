from picamera import PiCamera
from time import sleep

count = 0
while True:
    count+=1
    print('START')
    camera = None
    try:
        camera = PiCamera()
        # Take out this if no rotation is needed
        camera.rotation = 180
        print('Cam success')
    except:
        print("camera error")

    for i in range(10):
        print('Capture')
        camera.capture('./testing_' + str(i) + "_" + str(count) + '.jpg')
        sleep(.5)

    camera.close()
    print('DONE')
