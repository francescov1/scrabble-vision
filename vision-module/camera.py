from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep

def capture_image():
    camera = PiCamera()
    rawCapture=PiRGBArray(camera)
    camera.resolution = (3200,1800)
    #camera.framerate = 15
    camera.start_preview()
    sleep(5)
    camera.capture(rawCapture,format="bgr")
    sleep(1)
    Img = rawCapture.array
    camera.stop_preview()
    return Img



