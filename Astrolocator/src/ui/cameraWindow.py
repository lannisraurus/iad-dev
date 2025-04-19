"""
Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva
IST, 2025 - IAD

This file contains various methods to interface the camera.

"""

##################### Imports
from PyQt5.QtCore import *      # Basic Qt functionalities.
from PyQt5.QtWidgets import *   # GUI windows
from PyQt5.QtCore import *      # Qt threads, ...
from PyQt5.QtGui import *       # GUI Elements
import time
from datetime import datetime

try:
    from picamera2 import Picamera2
    from picamera2.previews.qt import QGlPicamera2
except:
    print('ERROR: Could not import QGlPicamera2 in cameraWindow!')

##################### Camera Window Class
class cameraWindow(QWidget):

    ############################################### Constructor
    def __init__(self, mainWindow):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('Astrolocator - Camera')

        mainWindow.logText("> Initializing Camera...\n")

        # Close Button
        self.closeButton = QPushButton("X")
        self.closeButton.setFixedSize(30, 20)
        self.closeButton.setStyleSheet(
            "font-weight: bold; border: none;"
        )
        self.closeButton.clicked.connect(self.close)

        # Camera
        try:
            self.cam = Picamera2()
            self.cam.post_callback = self.post_callback
            self.cam.configure(self.cam.create_preview_configuration(main={"size": (1024, 768)}))

            self.qpicamera2 = QGlPicamera2(self.cam, width=1024, height=768)
            self.qpicamera2.done_signal.connect(self.capture_done)

            mainWindow.logText("> Camera Objects created successfully.\n\n")

            self.cameraWorking = True
        except:
            mainWindow.logText("> ERROR: Could not initialize camera!\n\n")
            self.cameraWorking = False

        #Button
        self.captureButton = QPushButton("Exposure capture")
        self.captureButton.clicked.connect(self.do_capture)
        
        #Labels
        self.metadataLabel = QLabel()
        self.metadataLabel.setFixedWidth(400)
        self.metadataLabel.setAlignment(Qt.AlignTop)

        self.exposureLabel = QLabel("Exposure time (microseconds):")

        # Sliders
        self.exposureSlider = QSpinBox()
        self.exposureSlider.setMaximum(11760000)
        self.exposureSlider.setMinimum(1)

        self.titleLabel = QLabel("Camera")

        #Layout
        layout_v = QVBoxLayout()
        layout_h = QHBoxLayout()
        layout_htop = QHBoxLayout()
        layout_htop.addWidget(self.titleLabel, alignment=Qt.AlignTop | Qt.AlignLeft)
        layout_htop.addWidget(self.closeButton, alignment=Qt.AlignTop | Qt.AlignRight)
        layout_v.addLayout(layout_htop)
        

        if self.cameraWorking:
            layout_v.addWidget(self.qpicamera2, 80)
            layout_h.addWidget(self.captureButton)
            layout_h.addWidget(self.exposureLabel)
            layout_h.addWidget(self.exposureSlider)
            layout_v.addLayout(layout_h)
        
        self.resize(1200, 600)
        self.setLayout(layout_v)

        #Start camera
        if self.cameraWorking:
            self.cam.start()
        
    def post_callback(self, request):
        self.metadataLabel.setText(''.join(f"{k}: {v}\n" for k, v in request.get_metadata().items()))

    def do_capture(self):
        self.captureButton.setEnabled(False)
        cfg = self.cam.create_still_configuration()
        self.cam.stop()
        self.cam.configure(cfg)
        expTime = self.exposureSlider.value()
        self.cam.set_controls({"ExposureTime": expTime, "AeEnable": False})
        time.sleep(1)
        print("changed")
        self.cam.start()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.cam.capture_file(f"{timestamp}img.jpg", signal_function=self.qpicamera2.signal_done)

    def capture_done(self,job):
        self.cam.wait(job)
        self.cam.stop()
        self.cam.configure(self.cam.create_preview_configuration(main={"size": (1024, 768)}))
        self.cam.start()
        self.captureButton.setEnabled(True)

    ############################################### Events

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def paintEvent(self, event):
        # Draw the custom border around the window
        painter = QPainter(self)
        pen = QPen(QColor(170, 170, 170))  # Light gray color for the border
        pen.setWidth(2)  # Set border thickness
        painter.setPen(pen)
        painter.setBrush(Qt.transparent)
        
        # Draw the border around the window (excluding the title bar area)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)