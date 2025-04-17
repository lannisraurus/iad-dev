"""
Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva
IST, 2025 - IAD

This file contains the camera image.

"""
##################### Imports
from PyQt5.QtCore import *      # Basic Qt functionalities.
from PyQt5.QtWidgets import *   # GUI windows
from PyQt5.QtCore import *      # Qt threads, ...
from PyQt5.QtGui import *       # GUI Elements
from src.Camera import RPiCamera2
try:
    from picamera2.previews.qt import QGlPicamera2
except:
    print('ERROR: Could not import QGlPicamera2 in cameraWindow!')

##################### Commands Window Class
class cameraWindow(QWidget):

    ############################################### Constructor
    def __init__(self):
        # Intializing general stuff
        super().__init__()
        self.setFixedSize(1024,768)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('Astrolocator - Camera')

        # Layouts
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        # CAMERA IMAGE!
        self.camera = RPiCamera2()
        self.qpicamera2 = QGlPicamera2(self.camera.camera)

        self.mainLayout.addWidget(self.qpicamera2)



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


    ############################################### Camera

    def camera_on(self):
        self.camera.openPreview()
    
    def camera_off(self):
        self.camera.close()