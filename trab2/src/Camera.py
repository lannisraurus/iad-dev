"""
Grupo I, IAD, 2025
João Camacho, Duarte Tavares, Margarida Saraiva, Jorge Costa

This file contains various methods to interface with an
RPi camera.

"""

import time
from datetime import datetime

try:
    from picamera2 import Picamera2, Preview
except:
    print('ERROR in Camera: Could not import picamera2! Please install!')

################ Class
class RPiCamera2:
    
    def __init__(self, resolution=(1024, 768), framerate=30, autoBalance=False):
        
        try:
            self.camera = Picamera2()
        except:
            self.camera = None

        self.preview_config = self.camera.create_preview_configuration(
            main={"size": resolution})
        self.capture_config = self.camera.create_still_configuration(
            main={"size": resolution})
        self.video_config = self.camera.create_video_configuration(
            main={"size": resolution})

        if autoBalance:
            self.camera.set_controls({"AeEnable": True, "AwbEnable": True, "FrameRate": framerate})
        else:
            # Give time for Aec and Awb to settle, before disabling them
            time.sleep(1)
            self.camera.set_controls({"AeEnable": False, "AwbEnable": False, "FrameRate": framerate})
            # And wait for those settings to take effect
            time.sleep(1)

        return f"Camera initialized with resolution {resolution}, framerate {framerate} fps and auto balance = {autoBalance}."
    
    #exposure time in microsecs
    def changeSettings(self, framerate=30, autobalance=False, exposureTime=int(1000000/30), analogueGain=1.0):
        self.camera.set_controls({"AeEnable": autobalance, "AwbEnable": autobalance, "FrameRate": framerate,'ExposureTime': exposureTime, 'AnalogueGain': analogueGain})
        # Wait for those settings to take effect
        time.sleep(1)
        return self.camera.capture_metadata()

    def openPreview(self):
        try:
            self.camera.configure(self.preview_config)
            self.camera.start_preview(Preview.QTGL)
            return "Preview started."
        except Exception as e:
            return f"Error starting preview: {e}"

    def capture_image(self, filename="image.jpg", timestamp=False):
        self.camera.configure(self.capture_config)
        if timestamp:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{filename}"
        self.camera.capture_file(filename)
        print(f"Image saved as {filename}.")
    
    def capture_video(self, filename="video.h264", duration=10):
        self.camera.configure(self.video_config)
        self.camera.start_recording(filename)
        time.sleep(duration)  # Record for the specified duration
        self.camera.stop_recording()
        return f"Video saved as {filename}."
    
    def start_video(self, filename="video.h264"):
        self.camera.configure(self.video_config)
        self.camera.start_recording(filename)
        return f"Video started in {filename}."
    
    def end_video(self):
        self.camera.stop_recording()
        return f"Video finished."

    def close(self):
        self.camera.stop_preview()
        self.camera.close()
        return "Camera resources released."