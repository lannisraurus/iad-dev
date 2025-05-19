"""
Duarte Tavares, João Camacho, Jorge Costa, Margarida Saraiva
IST, 2025 - IAD

This file contains a settings window for location.

"""
##################### Imports
from PyQt5.QtCore import *      # Basic Qt functionalities.
from PyQt5.QtWidgets import *   # GUI windows
from PyQt5.QtCore import *      # Qt threads, ...
from PyQt5.QtGui import *       # GUI Elements

##################### Commands Window Class
class locationConfigWindow(QWidget):

    ############################### Constructor
    def __init__(self, mainWindow):
        
        self.mainWindow = mainWindow

        # Intializing general stuff
        super().__init__()
        self.setFixedSize(500,200)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('Astrolocator - Location Settings')

        # Buttons
        self.closeButton = QPushButton("X")
        self.closeButton.setFixedSize(30, 20)
        self.closeButton.setStyleSheet(
            "font-weight: bold; border: none;"
        )
        self.closeButton.clicked.connect(self.close)
        self.applyButton = QPushButton("Apply Changes")
        self.applyButton.clicked.connect(self.saveSettings)

        # Labels
        self.titleLabel = QLabel('Location Settings')
        self.latitudeLabel = QLabel('Latitude:')
        self.longitudeLabel = QLabel('Longitude:')
        self.altitudeLabel = QLabel('Altitude:')

        # User Input Lines
        self.latitudeConfig = QLineEdit()
        self.longitudeConfig = QLineEdit()
        self.altitudeConfig = QLineEdit()

        # Layouts
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.mainLayout)

        self.titleLayout = QHBoxLayout()
        self.titleLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.titleLayout)
        self.titleLayout.addWidget(self.titleLabel, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.titleLayout.addWidget(self.closeButton, alignment=Qt.AlignTop | Qt.AlignRight)

        self.latitudeLayout = QHBoxLayout()
        self.latitudeLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.latitudeLayout)
        self.latitudeLayout.addWidget(self.latitudeLabel, alignment=Qt.AlignTop)
        self.latitudeLayout.addWidget(self.latitudeConfig, alignment=Qt.AlignTop)

        self.longitudeLayout = QHBoxLayout()
        self.longitudeLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.longitudeLayout)
        self.longitudeLayout.addWidget(self.longitudeLabel, alignment=Qt.AlignTop)
        self.longitudeLayout.addWidget(self.longitudeConfig, alignment=Qt.AlignTop)

        self.altitudeLayout = QHBoxLayout()
        self.altitudeLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.altitudeLayout)
        self.altitudeLayout.addWidget(self.altitudeLabel, alignment=Qt.AlignTop)
        self.altitudeLayout.addWidget(self.altitudeConfig, alignment=Qt.AlignTop)

        self.applyLayout = QVBoxLayout()
        self.applyLayout.setAlignment(Qt.AlignBottom)
        self.mainLayout.addLayout(self.applyLayout)
        self.applyLayout.addWidget(self.applyButton, alignment=Qt.AlignBottom)


        # Load default settings
        self.mainWindow.logText('> Configuring Location Settings...\n')
        self.loadSettings()

        # Dragging window
        self.dragging = False

    ############################### Events

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

    ############################### Settings (saved in file "location_settings.txt")

    def loadSettings(self):
        try:
            file = open('assets/location_settings','r')
            self.mainWindow.logText('> Opened configuration file.\n')
        except:
            file = None
            self.mainWindow.logText('> Could not open configuration file!\n')

        try:
            self.latitudeConfig.setText(file.readline())
            self.longitudeConfig.setText(file.readline())
            self.altitudeConfig.setText(file.readline())
            self.mainWindow.logText('> Successfully loaded previous location settings.\n')
        except:
            self.latitudeConfig.setText('0')
            self.longitudeConfig.setText('0')
            self.altitudeConfig.setText('0')
            self.mainWindow.logText('> Could not load previous location settings. Please configure and apply settings!\n')
        
        if file:
            file.close()
        
        self.mainWindow.logText('\n')

    def saveSettings(self):
        try:
            file = open('assets/location_settings','w')
            file.write(self.latitudeConfig.text().strip('\n')+'\n')
            file.write(self.longitudeConfig.text().strip('\n')+'\n')
            file.write(self.altitudeConfig.text().strip('\n')+'\n')
            file.close()
            self.mainWindow.setTracker()
            self.mainWindow.logText('> Successfully saved and applied new location settings.\n\n')
        except:
            self.mainWindow.logText('> Something went wrong! Could not save new location settings!\n\n')

    def getSettings(self):
        return (float(self.latitudeConfig.text()), float(self.longitudeConfig.text()), float(self.altitudeConfig.text()))