import time
from picamera2 import Picamera2, Preview

class RPiCamera2:
    def __init__(self, resolution=(1024, 768), framerate=30, autoBalance=false):
        self.camera = Picamera2()

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

        return f"Camera initialized with resolution {resolution}, framerate {framerate} fps and {if (not autoBalance) "no " else ""}auto balance."
    
    #exposure time in microsecs
    def changeSettings(framerate=30, autobalance=false, exposureTime=int(1000000/30), analogueGain=1.0):
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

    def capture_image(self, filename="image.jpg", timestamp=false):
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
    
    def close(self):
        self.camera.stop_preview()
        self.camera.close()
        return "Camera resources released."