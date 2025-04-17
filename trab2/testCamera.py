from src.Camera import RPiCamera2
import time

cam = RPiCamera2()
cam.openPreview()
time.sleep(10)